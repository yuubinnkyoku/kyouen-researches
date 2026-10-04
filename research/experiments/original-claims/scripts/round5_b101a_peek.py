from pathlib import Path
p = Path(r"D:\ghq\github.com\yuubinnkyoku\kyouen-researches\research\experiments\original-claims\output\round4_b092.json")
text = p.read_text()
idx = text.find("defo")
print("defo at", idx)
print(text[idx:idx+2500] if idx >= 0 else "no defo")
