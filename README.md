מערכת Keylogger
פרויקט זה מדגים מערכת Keylogger מלאה, המורכבת משלושה חלקים עיקריים:

KeyloggerAgent (הסוכן) – רץ על מחשב היעד, מאזין להקשות מקלדת, מצפין אותן ושולח לשרת.
Server – אפליקציית Flask המקבלת ושומרת את הנתונים (בפורמט CSV), ומספקת API לתצוגת ה-Front.
Front – ממשק משתמש (HTML/CSS/JS) המציג את הנתונים, מאפשר לבחור מחשב מעקב, לבצע חיפוש לוגים ועוד.


מבנה הפרויקט
keylogger/
├─ KeyloggerAgent/
│ ├─ Encryption.py
│ ├─ KeyloggerManager.py
│ ├─ KeyloggerService.py
│ ├─ Write.py
│ ├─ .env (לא מועלה ל-GitHub – מכיל סיסמאות/הגדרות)
│ └─ ...
├─ server/
│ ├─ app.py
│ ├─ routes.py
│ ├─ controllers.py
│ ├─ computers/ (תיקייה נדרשת לאחסון קבצי CSV למחשבים שונים)
│ ├─ .env (לא מועלה ל-GitHub – מכיל סיסמאות/הגדרות)
│ └─ ...
├─ front/
│ ├─ index.html
│ ├─ index.css
│ └─ index.js
└─ README.md

קבצי .env
גם בצד הסוכן (KeyloggerAgent) וגם בצד השרת (Server) יש צורך בקובץ .env נפרד, המכיל משתנים רגישים כגון סיסמת ההצפנה וכתובת השרת. אין להעלות את הקבצים הללו ל-GitHub (לרוב נמנעים מכך בעזרת קובץ .gitignore).

דוגמה לקובץ .env ב-KeyloggerAgent
PASSWORD='098897787'
SERVER_NAME='127.0.0.1:5555'

PASSWORD: מחרוזת המשמשת להצפנה (למשל XOR).
SERVER_NAME: כתובת (host:port) של השרת שאליו נשלחות ההקשות.
דוגמה לקובץ .env בצד השרת
PASSWORD='098897787'


PASSWORD: חייב להתאים לסיסמה שבסוכן, לצורך פענוח הנתונים הנשלחים.

התיקייה computers בשרת
בתוך תיקיית server, יש ליצור תיקייה בשם computers לפני הרצת השרת. שם יישמרו קבצי CSV עבור כל מחשב (לפי כתובת MAC). אם התיקייה לא קיימת, השרת לא יוכל לאחסן את הלוגים.

התקנה ושימוש
1. התקנת והפעלת השרת
ודא שיש לך Python 3 מותקן.
התקן ספריות פייתון נדרשות (למשל Flask, Flask-Cors, pandas, python-dotenv):
pip install flask flask-cors pandas python-dotenv
בתיקיית server, צור את התיקייה computers (אם לא קיימת).
צור או עדכן קובץ .env בתיקיית server (לא עולה ל-GitHub), לדוגמה:
PASSWORD='098897787'
הרץ:
python app.py
ברירת המחדל: השרת יאזין בכתובת http://127.0.0.1:5555/
2. התקנת והפעלת הסוכן (KeyloggerAgent)
ודא שיש לך Python 3.
התקן את הספריות הנדרשות (pynput, requests, python-dotenv וכו'):
pip install pynput requests python-dotenv
צור/ערוך קובץ .env בתיקיית KeyloggerAgent, לדוגמה:
PASSWORD='0988977872186763'
SERVER_NAME='127.0.0.1:5555'
PASSWORD תואם לזה שבשרת.
SERVER_NAME זה host:port שבו השרת מאזין.
הרץ:
python KeyloggerManager.py
כעת הסוכן יאזין להקשות וישלח אותן לשרת.
3. השימוש בממשק (Front)
תיקיית front מכילה:
index.html
index.css
index.js
אם Flask מוגדר להגיש את הקבצים הסטטיים מהתיקייה front, ניתן לפתוח דפדפן לכתובת http://127.0.0.1:5555/ ולהגיע לממשק.
בממשק ניתן לבחור מחשב (כתובת MAC) מרשימה, ולצפות בלוגים המגיעים מהשרת.
איך המערכת עובדת
שרת – מקבל נתונים מקודדים (XOR) בנתיב /api/storage ושומר אותם בקבצי CSV בתיקיית computers.
סוכן – לוכד הקשות, מצפין אותן ב-XOR ושולח POST לשרת כל כמה שניות.
Front – מושך רשימת מחשבים (/api/get_users) ומידע (/api/get_data/<mac>) ומציג אותם בחלוקה לפי חלון, זמן ותוכן.
