// W33: minimal CaDiCaL driver used by ladder_drat_native.py.
//
// The standalone `cadical` binary cannot apply per-variable decision phases
// (`Solver::phase`), which the pysat receipt path sets from the warm-start
// candidate.  This shim links the same libcadical.a and exposes exactly the
// API calls the receipt needs, so the proof is still written by the native
// tracer straight to disk (never buffered in RAM by the caller).
//
// usage:
//   native_solve <input.cnf> <proof> <conflict-budget>
//                <phases|-|> <result.json|-> <witness|-> [<whether phases file is on>]
//
// The phases file is whitespace-separated signed literals passed verbatim to
// Solver::phase(lit).  Exit code is CaDiCaL's: 10 SAT, 20 UNSAT, 0 UNKNOWN.
// proof tracing is opened before read_dimacs because the API only allows it in
// state CONFIGURING.
#include "cadical.hpp"

#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <ctime>
#include <sys/resource.h>

static double monotonic_seconds (void) {
  struct timespec ts;
  clock_gettime (CLOCK_MONOTONIC, &ts);
  return ts.tv_sec + 1e-9 * ts.tv_nsec;
}

int main (int argc, char **argv) {
  if (argc < 4) {
    fprintf (stderr,
             "usage: %s <input.cnf> <proof> <conflict-budget> "
             "[<phases>|-] [<result.json>|-] [<witness>|-]\n",
             argv[0]);
    return 2;
  }
  const char *input = argv[1];
  const char *proof = argv[2];
  const int budget = atoi (argv[3]);
  const char *phases_path =
      (argc > 4 && strcmp (argv[4], "-")) ? argv[4] : (const char *) 0;
  const char *result_path =
      (argc > 5 && strcmp (argv[5], "-")) ? argv[5] : (const char *) 0;
  const char *witness_path =
      (argc > 6 && strcmp (argv[6], "-")) ? argv[6] : (const char *) 0;

  CaDiCaL::Solver solver;

  if (!solver.trace_proof (proof)) {
    fprintf (stderr, "native_solve: cannot open proof '%s'\n", proof);
    return 2;
  }

  int vars = 0;
  const char *error = solver.read_dimacs (input, vars, 1);
  if (error) {
    fprintf (stderr, "native_solve: read_dimacs: %s\n", error);
    return 2;
  }

  long phase_hints = 0;
  if (phases_path) {
    FILE *file = fopen (phases_path, "r");
    if (!file) {
      fprintf (stderr, "native_solve: cannot open phases '%s'\n", phases_path);
      return 2;
    }
    int lit;
    while (fscanf (file, "%d", &lit) == 1) {
      solver.phase (lit);
      phase_hints++;
    }
    fclose (file);
  }

  if (budget > 0)
    solver.limit ("conflicts", budget);

  const double started = monotonic_seconds ();
  const int res = solver.solve ();
  const double elapsed = monotonic_seconds () - started;

  const long long conflicts = solver.get_statistic_value ("conflicts");
  const long long decisions = solver.get_statistic_value ("decisions");
  const long long propagations = solver.get_statistic_value ("propagations");
  const long long ticks = solver.get_statistic_value ("ticks");

  if (res == 10 && witness_path) {
    FILE *file = fopen (witness_path, "w");
    if (!file) {
      fprintf (stderr, "native_solve: cannot write witness '%s'\n", witness_path);
      return 2;
    }
    fprintf (file, "s SATISFIABLE\nv");
    for (int var = 1; var <= vars; ++var)
      fprintf (file, " %d", solver.val (var) > 0 ? var : -var);
    fprintf (file, " 0\n");
    fclose (file);
  }

  solver.close_proof_trace (true);
  solver.statistics ();

  struct rusage usage;
  getrusage (RUSAGE_SELF, &usage);

  if (result_path) {
    FILE *file = fopen (result_path, "w");
    if (!file) {
      fprintf (stderr, "native_solve: cannot write result '%s'\n", result_path);
      return 2;
    }
    fprintf (file, "{\n");
    fprintf (file, "  \"solver\": \"cadical-native\",\n");
    fprintf (file, "  \"solver_version\": \"%s\",\n", CaDiCaL::Solver::version ());
    fprintf (file, "  \"solver_exit_code\": %d,\n", res);
    fprintf (file, "  \"variables\": %d,\n", vars);
    fprintf (file, "  \"conflict_budget\": %d,\n", budget);
    fprintf (file, "  \"phase_hints\": %ld,\n", phase_hints);
    fprintf (file, "  \"solve_seconds\": %.6f,\n", elapsed);
    fprintf (file, "  \"statistics\": {\"conflicts\": %lld, \"decisions\": %lld, "
                   "\"propagations\": %lld, \"ticks\": %lld},\n",
             conflicts, decisions, propagations, ticks);
    fprintf (file, "  \"max_rss_kb\": %ld\n", usage.ru_maxrss);
    fprintf (file, "}\n");
    fclose (file);
  }
  return res;
}
