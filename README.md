# HScProject
Extracting Info the https://www.themoviedb.org using APIs, and mapping & visualizing place of birth - popularity.
 ## Intro - Background
כחלק מתקנות שהוצעו לתיקון חברה ולשאוף לשוויון אמיתי – הקולנוע מהווה חלק בלתי נפרד. 

כתוצאה מכך תרבות הקולנוע הושפעה רבות מכיוון שלקולנוע מספר תפקידים חשובים ועיקריים, לדוגמא:
- הקלונוע מהווה תפקיד בהצגת מעמדות בחברה
- הקולנוע מכתיב נורמות חברתיות
- שחקני קולנוע זוכים לפרסום רב ומהווים מודל לחיקוי להרבה אנשים
- חשיפה לאוכלוסיות שונות באולכוסייה ובכך משמש מקור מידע גדול ורבגוני

## Goal

בשנים האחרונות אנו עדים לשינויים בתרבות הקולנוע. לדוגמא :

האקדמיה האמריקנית לקולנוע קבעה שהחל מ2024 כדי שסרט יוכל להגיש מועמדות לסרט הטוב באוסקר –
לפחות אחד מהשחקנים הראשיים או המשניים יהיה אסיאתי, היספני, שחור, צפון אפריקאי, מזרח תיכוני או 
יליד. 

לאור שינויים מסוג זה מטרתינו היא לחקור האם קיים קשר בין מיקום הלידה של שחקן קולנוע לבין הצלחתו (הפופולריות שלו) .

מטרה נוספת היא ללמוד להשתמש במידע רב , להסיק מידע ממקורות חצי מובנים – בין אם בהצלבת מידע ובין אם בשימוש בכלים כגון openRefine .

ומטרתינו הסופית היא להציג את התוצאות והמסקנות באמצעות ויזואליזציה – על מפת ארצות הברית.

## Work plan

בשלב הראשון נבנה רשימה של כל השחקנים האמריקאים ומקום לידתם באמצעות API של TMDB בשפת פייתון בפרוטוקול HTTP .

(כך שיחידת המידע שלנו תהיה :שם השחקן , מקום לידתו והפופולריות שלו)

לאחר מכן , נחשב פופולריות עבור כל שחקן מהרשימה באופן הבא :

- נעבור על רשימת הסרטים בהם הוא השתתף ובעבור כל סרט – נחשב :

***ציון הסרט*** (מנורמל) * ***מספר מדרגים*** * ***גודל התפקיד שלקח בסרט.***

את **ציון הסרט ומספר המדרגים** מIMDB/TMDB בעזרת הAPI שכתבנו לעיל.
  
על מנת לחשב את **גודל התפקיד** – נעבור ונעבד את התמליל של הסרט באמצעות סקריפטים בפייתון ונחשב את היחס בין כמות המילים של השחקן ביחס לסך המילים בסרט.
  
- לבסוף, נציג את המידע שאספנו עד כה על מפת ארה"ב כך שנוכל להבחין האם יש קשר בין מיקום הלידה לבין כמות ומידת הפופולוריות של השחקנים.

## Expectation
אנו משערים שנמצא קשר (בין אם חלש או חזק) בין מקום הלידה לבין מידת הפופולריות שלו מכמה סיבות :

1. תרבות הקולנוע האמריקאית מתכנסת ברובה סביב הוליווד – דבר שמוביל להגירה לאיזור זה – וכך צאצאים של שחקנים מצליחים שבחרו בקריירת משחק יוולדו בהוליווד עם פוטנציאל גבוה יותר להצלחה – בין אם בגלל המיקום ובין בגלל הקשרים של הוריהם.
2. רמת החשיפה שונה במקומות שונים, דבר הגורם לפערים בביקוש והיצע בתחום ובקריירת המשחק.
3. במדינות עניות יותר ישנן פחות הזדמנויות ויש קושי רב יותר במציאת עבודה בתחום הקולנוע, דבר שעלול לעכב את התפתחות הקריירה של אותם שחקנים ולפגוע בפופולריות שלהם.
4. בסרטים רבים אין צורך בגיוון של אוכלוסיות ותרבויות בהרכב השחקנים בסרט - דבר שיכול להביא להרכב שחקנים מאותו מיקום.


## Bibliography

- TMDB - https://www.themoviedb.org/?language=en
- IMDB - https://www.imdb.com/?ref_=nv_home
- IMSDB - https://imsdb.com/
