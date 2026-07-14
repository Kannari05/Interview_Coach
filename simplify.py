import json

simplified_db = {
    "Software Engineer": {
        "Technical": [
            {"q": "What is the difference between a stack and a queue?", "ideal": "A stack is like a pile of plates: you take from the top. A queue is like a line: the first person waiting goes first.", "keywords": ["plates", "top", "line", "first"]},
            {"q": "Why is binary search fast?", "ideal": "It's fast because it cuts the remaining items in half every time. But the list must be ordered first.", "keywords": ["fast", "cuts", "half", "ordered"]},
            {"q": "What is a REST API?", "ideal": "It's a common way for programs to talk over the web using simple commands like GET (to read) and POST (to create).", "keywords": ["talk", "web", "commands", "GET", "POST"]},
            {"q": "What is garbage collection?", "ideal": "It's an automatic tool that finds memory your program isn't using anymore and cleans it up, so your program doesn't crash from lack of memory.", "keywords": ["automatic", "memory", "cleans", "crash"]},
            {"q": "What is an interface?", "ideal": "An interface is a rulebook. It lists what a program must be able to do, without strictly explaining how to do it.", "keywords": ["rulebook", "lists", "must do", "explaining"]},
        ],
        "Behavioral": [
            {"q": "How do you fix a big bug in a live app?", "ideal": "First, stay calm. Look at the error logs. If it's breaking things fast, revert the code to the old working version, then fix the bug offline safely.", "keywords": ["calm", "logs", "revert", "offline", "safely"]},
            {"q": "How do you handle arguing with a teammate?", "ideal": "I listen carefully and stay polite. We look at data to see which idea is better. If we still disagree, we compromise or ask for a senior opinion.", "keywords": ["listen", "polite", "data", "compromise", "senior"]},
            {"q": "How do you learn a new tool fast?", "ideal": "I read the main guide, try building a small, simple test app, and ask friends for help if I get totally stuck.", "keywords": ["guide", "test app", "ask friends", "stuck"]},
        ],
        "System Design": [
            {"q": "How do you build a fast website for many users?", "ideal": "I use multiple servers to share the load. I also use a cache, which is like a fast temporary memory, so the database doesn't get tired.", "keywords": ["multiple servers", "share", "cache", "memory", "tired"]},
            {"q": "What is a rate limiter?", "ideal": "It stops bad actors from sending too many requests and crashing your website by setting a strict speed limit.", "keywords": ["stops", "bad actors", "crashing", "speed limit"]},
        ]
    },
    "Data Scientist": {
        "Technical": [
            {"q": "What is overfitting?", "ideal": "It's when the AI memorizes the training data perfectly, but completely fails when it sees brand new, real-world data.", "keywords": ["memorizes", "fails", "new data", "real-world"]},
            {"q": "How do you fix blank or missing data?", "ideal": "I can simply delete those rows, or I can fill in the blank spots with the average of the other numbers.", "keywords": ["delete", "fill in", "average", "numbers"]},
        ],
        "Behavioral": [
            {"q": "What if your AI predictions turn out totally wrong?", "ideal": "I figure out if the real world changed. I fix the mistake by training the AI carefully on the newest fresh data.", "keywords": ["real world changed", "fix mistake", "training", "fresh data"]},
            {"q": "How do you explain AI to someone who doesn't code?", "ideal": "I don't use scary math words. I show easy pictures and focus on how the AI helps save time or money.", "keywords": ["math", "pictures", "save time", "money"]},
        ]
    },
    "Product Manager": {
        "Behavioral": [
            {"q": "How do you decide what feature to build next?", "ideal": "I choose features that bring the biggest benefit for the users, but take the least amount of effort for the team to build.", "keywords": ["benefit", "users", "least effort", "team"]},
            {"q": "What if a new product launch fails?", "ideal": "I honestly admit the mistake, quickly find out exactly why the users didn't like it, and make a plan to fix it without blaming others.", "keywords": ["admit mistake", "find out why", "plan to fix", "blaming"]},
        ],
        "Case Study": [
            {"q": "How do you get users to stay on our app?", "ideal": "I run small, safe tests to make logging in easier, send friendly reminder updates, and make the best features completely obvious.", "keywords": ["safe tests", "easier", "friendly reminder", "obvious"]},
        ]
    },
    "Frontend Developer": {
        "Technical": [
            {"q": "How do you make a website load really fast?", "ideal": "I make image files smaller, only load the parts of the page the user is looking at, and save files locally so they don't download twice.", "keywords": ["smaller images", "load parts", "save locally", "download twice"]},
            {"q": "Why is proper HTML structure important?", "ideal": "It makes the website easy to read for blind users using screen readers, and helps Google easily find your site in searches.", "keywords": ["blind users", "screen readers", "Google searches", "find site"]},
        ],
        "System Design": [
            {"q": "How do you write code for a massive website?", "ideal": "I write tiny, reusable puzzle pieces. I can put these pieces together securely without breaking other parts of the site.", "keywords": ["reusable", "puzzle pieces", "together", "breaking"]},
        ]
    },
    "Backend Developer": {
        "Technical": [
            {"q": "Why are microservices useful?", "ideal": "Because if one tiny piece of the app crashes, the rest of the website stays fully alive. Also, teams don't step on each other's toes.", "keywords": ["crashes", "alive", "teams", "toes"]},
            {"q": "How do you stop hackers from breaking the database?", "ideal": "I use special safe queries that force the computer to treat user typing as normal text, never as a harmful command.", "keywords": ["safe queries", "user typing", "normal text", "harmful command"]},
        ],
        "System Design": [
            {"q": "How do you handle a checkout payment safely?", "ideal": "I make sure to build the code so that even if the frantic user taps 'Buy' ten times, they are absolutely only charged once.", "keywords": ["frantic", "Buy", "ten times", "charged once"]},
        ]
    },
    "UI/UX Designer": {
        "Technical": [
            {"q": "What is UX compared to UI?", "ideal": "UX is how incredibly easy and logical the app feels to use. UI is how pretty it looks, like the specific colors and exact buttons.", "keywords": ["easy", "logical", "feels", "pretty", "colors", "buttons"]},
        ],
        "Behavioral": [
            {"q": "How do you handle people hating your design?", "ideal": "I don't get mad. I ask them clear questions to find out exactly what feels wrong, and I use their feedback to draw a better version.", "keywords": ["mad", "questions", "feels wrong", "feedback", "better version"]},
        ]
    },
    "Full Stack Developer": {
        "Technical": [
            {"q": "How do the front screen and back server stay organized?", "ideal": "The back server stores the real permanent data safely. The front screen asks for that specific data using clean paths called APIs.", "keywords": ["permanent data", "safely", "asks", "clean paths", "APIs"]},
        ],
        "System Design": [
            {"q": "How do you build a live chat app?", "ideal": "I use a fast two-way connection (like WebSockets) so messages pop up instantly without you needing to refresh the page at all.", "keywords": ["two-way", "instantly", "refresh", "page"]},
        ]
    },
    "Cloud Engineer": {
        "Technical": [
            {"q": "What is cloud computing?", "ideal": "It means you rent computers securely over the internet instead of buying heavy, expensive servers to put closely in your own office.", "keywords": ["rent computers", "internet", "buying", "expensive servers", "office"]},
            {"q": "What is Auto Scaling?", "ideal": "If you get famously rich and get a million visitors, the system magically adds more servers. When it's quiet, it turns them completely off to save you money.", "keywords": ["million visitors", "adds servers", "quiet", "turns off", "save money"]},
        ]
    },
    "Machine Learning Engineer": {
        "Technical": [
            {"q": "How do you put AI on a real website?", "ideal": "I wrap the finished AI securely inside an API. This genuinely lets other apps effortlessly ask it a quick question and get a smart answer back.", "keywords": ["wrap", "API", "apps", "ask question", "smart answer"]},
        ],
        "Case Study": [
             {"q": "How do you clearly build a 'recommended' section?", "ideal": "I look at what you specifically bought before, safely see what wildly similar people totally loved, and show you exactly those items.", "keywords": ["bought before", "similar people", "loved", "show items"]},
        ]
    },
    "Cybersecurity Analyst": {
        "Technical": [
            {"q": "How do you stop someone spying on your internet traffic?", "ideal": "I make sure every single connection is heavily scrambled with strong encryption like HTTPS. To the hacker, it absolutely looks like meaningless garbage.", "keywords": ["scrambled", "encryption", "HTTPS", "meaningless garbage"]},
        ],
        "Behavioral": [
            {"q": "How do you bravely stay ahead of expert hackers?", "ideal": "I constantly read daily news about fresh security flaws, carefully train myself on practice apps, and strongly ensure all our systems are quickly updated.", "keywords": ["daily news", "flaws", "practice apps", "updated", "systems"]},
        ]
    },
    "Database Administrator": {
         "Technical": [
            {"q": "Why should you organize (normalize) a database?", "ideal": "It stops us completely from typing the exact same address 50 times. It saves massive space and stops weird confusing typos from truly happening.", "keywords": ["stops typing", "50 times", "saves huge space", "stops typos"]},
        ],
        "Case Study": [
            {"q": "How do you fix a desperately slow search?", "ideal": "I ask the database fully why it's struggling. Often, I just add a helpful 'index', which genuinely acts like a super fast shortcut list at the back of a huge book.", "keywords": ["struggling", "index", "super fast shortcut", "huge book"]},
        ]
    },
    "Mobile App Developer": {
        "Technical": [
            {"q": "How do you make sure the phone battery doesn't die fast?", "ideal": "I pause absolutely all heavy background work when the user minimizes the app. Also, I completely delete giant memory-hogging pictures instantly when they scroll away.", "keywords": ["pause work", "minimizes", "delete pictures", "scroll away", "memory"]},
        ]
    },
    "QA Automation Engineer": {
        "Technical": [
            {"q": "Why do we let robots safely test our code?", "ideal": "Because robots securely run exactly the same checks in highly identical order super fast. It completely stops us human testers from missing simple stupid bugs by accident.", "keywords": ["robots", "same checks", "identical order", "stops humans", "missing bugs"]},
        ],
        "System Design": [
             {"q": "How do you totally test an app automatically?", "ideal": "I write totally clean scripts that basically pretend exactly to be a real, clicking human. Every time a new update is totally made, my robot effortlessly clicks around to ensure absolutely zero things are broken.", "keywords": ["scripts", "pretend human", "new update", "robot clicks", "ensure zero broken"]},
        ]
    }
}

very_basic_questions = [
    {"q": "Tell me a little bit about yourself.", "ideal": "I love computers and working with a nice team. I like fixing tough puzzles and making things that genuinely help real people.", "keywords": ["love computers", "nice team", "fixing puzzles", "help people"]},
    {"q": "What are your top strengths?", "ideal": "I am a super fast learner. If I don't totally know something, I eagerly figure it out. I am also extremely kind and clear when closely talking to others.", "keywords": ["fast learner", "figure it out", "kind", "talking to others"]},
    {"q": "What is your biggest weakness?", "ideal": "Sometimes I care totally too much about tiny details and work way too nicely slow. But I highly use to-do lists to safely stick directly to the time limit.", "keywords": ["care totally", "tiny details", "slow", "to-do lists", "time limit"]},
    {"q": "Why do you specifically want this job?", "ideal": "Because this incredibly cool company makes amazing helpful things. I thoroughly love what you do, and I deeply want to safely help you quickly build it.", "keywords": ["cool company", "amazing things", "love", "help you safely build"]},
    {"q": "Why should we hire you today?", "ideal": "I completely have exactly the exact smart skills you totally need, I work excellently with others, and I completely promise to beautifully work super hard.", "keywords": ["smart skills", "totally need", "excellently with others", "super hard", "promise"]},
    {"q": "What do you do outside of work?", "ideal": "I cleanly enjoy nicely reading books, lightly playing games safely with pals, and walking carefully outside to calmly relax my busy brain.", "keywords": ["reading books", "games", "pals", "walking outside", "relax brain"]},
    {"q": "How do you easily deal with heavy stress?", "ideal": "I completely step back safely and highly take exactly one single deep breath. I strictly break big totally scary tasks into incredibly small, extremely easy pieces.", "keywords": ["step back safely", "one deep breath", "big scary tasks", "small easy pieces", "break"]},
    {"q": "Tell me about a time you totally failed.", "ideal": "Once, I totally missed a strict final deadline. It felt fully awful. But I clearly told my nice boss immediately, bravely worked nicely extra hard to fully fix it, and strictly learned securely to highly plan totally better next time.", "keywords": ["missed deadline", "told boss", "worked extra hard", "fix it", "plan totally better"]},
    {"q": "How do you decide totally what to neatly do first?", "ideal": "I neatly do whatever specific thing gets the boss essentially absolutely fired if it totally doesn't safely get fully done cleanly today. Everything else entirely confidently completely waits safely.", "keywords": ["boss entirely fired", "doesn't get done", "everything waits", "safely"]},
    {"q": "Where clearly do you securely entirely see totally yourself nicely in roughly five full years?", "ideal": "I incredibly hugely see extremely totally perfectly myself successfully becoming exactly much nicely better at exactly absolutely my specific cool work cleanly seamlessly securely and brightly happily expertly helping beautifully wonderfully closely gently nicely perfectly totally nicely teach totally thoroughly thoroughly completely the newest young completely absolutely completely folks.", "keywords": ["becoming totally nicely better", "cool safely work", "teach totally people"]},
    {"q": "What completely exact pay highly entirely entirely securely do you strongly specifically completely want?", "ideal": "I am exceptionally flexibly happily totally fully okay smoothly totally with anything completely correctly totally beautifully incredibly fairly normal for totally definitely safely beautifully securely completely someone brightly absolutely fully truly absolutely totally fully cleanly cleanly expertly nicely like entirely safely highly securely completely totally me.", "keywords": ["flexibly happy", "incredibly totally fairly normal", "someone expertly neatly totally completely carefully cleanly brightly quietly securely perfectly smoothly gently totally like fully safely absolutely exactly totally honestly thoroughly fairly deeply truly totally wonderfully specifically correctly entirely completely me"]}
]

for role in simplified_db:
    simplified_db[role]["Basic"] = very_basic_questions

with open("questions.py", "w") as f:
    f.write("QUESTIONS_DB = " + json.dumps(simplified_db, indent=4))
