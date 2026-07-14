import json

# Refined, easily understandable, "moderate" answers
existing_db = {
    "Software Engineer": {
        "Technical": [
            {"q": "Explain the difference between a stack and a queue.", "ideal": "Think of a stack like a pile of books: the last book you put on top is the first one you take off. This is called LIFO (Last In, First Out). A queue is exactly like waiting in line at a store: the first person in line is the first one served (First In, First Out, or FIFO).", "keywords": ["LIFO", "FIFO", "stack", "queue", "last", "first"]},
            {"q": "What is the time complexity of binary search?", "ideal": "It has an O(log n) time complexity. Basically, this means it's super fast because it cuts the search area in half every single step. Just remember that the list has to be sorted first for it to work.", "keywords": ["O(log n)", "sorted", "half", "fast", "search area"]},
            {"q": "Describe RESTful API principles.", "ideal": "REST is a set of rules for web services to talk to each other. The biggest rule is 'statelessness', meaning each request has all the info needed to process it. We use simple HTTP actions like GET to read data, POST to create it, and DELETE to remove it.", "keywords": ["statelessness", "rules", "HTTP", "GET", "POST", "DELETE"]},
            {"q": "How does garbage collection work in Java or Python?", "ideal": "Garbage collection is a background process that automatically cleans up memory. Instead of the programmer having to manually delete objects they are done using, the system spots items that aren't being used anymore and safely deletes them to free up space.", "keywords": ["background process", "memory", "automatically", "cleans", "deletes"]},
            {"q": "What is the difference between an abstract class and an interface?", "ideal": "An abstract class can include some actual, working code that other classes can share. An interface is more like a strict contract: it simply lists the required action names without providing any actual code, ensuring other classes follow the rules.", "keywords": ["working code", "contract", "share", "rules", "required"]},
        ],
        "Behavioral": [
            {"q": "Tell me about a time you debugged a critical production issue.", "ideal": "A good approach is to stay calm and follow the STAR method. I would explain the situation, how I quickly found the error logs, the exact fix I applied or how I rolled back the update, and finally how we communicated the fix to our users to maintain trust.", "keywords": ["calm", "logs", "fix", "rolled back", "communicated", "trust"]},
            {"q": "How do you handle disagreements with teammates on technical decisions?", "ideal": "I believe in keeping things respectful and focusing on facts. I listen to their ideas, present data or small tests to compare options, and aim for a compromise. If we still can't agree, I'm happy to ask a senior engineer for a fresh perspective.", "keywords": ["respectful", "facts", "listen", "data", "compromise", "perspective"]},
            {"q": "Describe a time when you had to learn a new technology quickly.", "ideal": "I focus on the practical basics first. I read the official documentation, quickly build a tiny test project so I can learn hands-on, and ask experienced teammates whenever I get stuck. Learning by doing is my most effective strategy.", "keywords": ["practical", "basics", "documentation", "test project", "hands-on", "doing"]},
        ],
        "System Design": [
            {"q": "Design a URL shortening service like bit.ly.", "ideal": "I'd use a simple database to pair long URLs with short generated codes. To make it extremely fast, I would put a caching layer (like Redis) in front so popular links load instantly. I'd also add a load balancer to handle high traffic smoothly.", "keywords": ["database", "short codes", "caching", "Redis", "load balancer", "traffic"]},
            {"q": "How would you design a rate limiter?", "ideal": "A rate limiter stops users from overwhelming a system. I would track user requests using a fast memory store like Redis. If a user sends too many requests within a specific time window, the system gently blocks them until the timer resets.", "keywords": ["overwhelming", "track", "Redis", "time window", "blocks", "resets"]},
        ]
    },
    "Data Scientist": {
        "Technical": [
            {"q": "Explain overfitting and how to prevent it.", "ideal": "Overfitting is like memorizing the answers for a test without understanding the subject; the model performs perfectly on training data but fails terribly on real-world data. We prevent it by keeping the model simple, using more training data, or stopping the training early before it memorizes the noise.", "keywords": ["memorizing", "fails", "real-world", "simple", "more data", "stopping early"]},
            {"q": "What is the difference between bagging and boosting?", "ideal": "Bagging builds many independent models at the same time and averages their guesses to get a solid answer (like asking a crowd). Boosting builds models one after another, where each new model tries to fix the specific mistakes made by the previous one.", "keywords": ["averages", "crowd", "one after another", "fix mistakes", "previous"]},
            {"q": "How do you handle missing or corrupted data in a dataset?", "ideal": "First, I figure out why it's missing. If a whole column is mostly empty, I might just drop it. Otherwise, I can fill in the blanks by taking the average of the other numbers, or use a machine learning tool to make a smart guess for what goes there.", "keywords": ["why", "drop", "fill in", "average", "smart guess"]},
        ],
        "Behavioral": [
            {"q": "Describe a project where your model had unexpected results.", "ideal": "I would explain what happened and why I think the data changed over time (concept drift) or if there was a bug in how we processed the data. Then, I’d talk about the steps I took to quickly retrain the model and improve our monitoring.", "keywords": ["data changed", "concept drift", "bug", "retrain", "improve monitoring"]},
            {"q": "How do you explain complex technical concepts to non-technical stakeholders?", "ideal": "I completely drop the math jargon and focus on exactly how the model helps the business make money or save time. I use simple visual charts, and everyday analogies to explain how the AI makes decisions.", "keywords": ["drop jargon", "business", "save time", "visual charts", "analogies"]},
        ],
        "Case Study": [
            {"q": "How would you build a churn prediction model?", "ideal": "Churn prediction identifies customers likely to leave. I'd grab data like how often they log in and their billing history. Since most people don't churn, I'd balance the data carefully, train a dependable model like Random Forest, and track how well it catches the at-risk users.", "keywords": ["leave", "log in", "billing", "balance", "Random Forest", "at-risk"]},
        ]
    },
    "Product Manager": {
        "Behavioral": [
            {"q": "Tell me about a product you shipped from idea to launch.", "ideal": "I like to outline the full journey: talking to users to find a real problem, deciding what core features to build first, working closely with developers and designers to build it, and finally checking the success metrics after launch.", "keywords": ["talking to users", "core features", "designers", "developers", "success metrics", "launch"]},
            {"q": "How do you prioritize features when everything seems urgent?", "ideal": "I rely on simple frameworks that measure the potential impact of a feature versus how much effort it takes to build. I talk to stakeholders, look at user data, and focus solidly on whatever moves us closest to our company goals.", "keywords": ["impact", "effort", "stakeholders", "user data", "company goals"]},
            {"q": "Describe a time when a product launch failed. What did you learn?", "ideal": "I'd honestly share what went wrong--whether we misunderstood what users wanted or had a confusing marketing message. The most important part is how we quickly gathered feedback, fixed the issues, and created a better testing process for next time.", "keywords": ["went wrong", "misunderstood", "feedback", "fixed", "testing process"]},
        ],
        "Case Study": [
            {"q": "How would you improve our mobile app's user retention?", "ideal": "I'd start by looking at analytics to see exactly where users are abandoning the app. Then, I would run small A/B tests on things like a smoother signup process or sending a helpful push notification, checking the 30-day return rate.", "keywords": ["analytics", "abandoning", "A/B tests", "signup", "push notification", "return rate"]},
            {"q": "Design an elevator system for a 100-story building.", "ideal": "I'd first define the main goal: reducing wait times during busy morning hours. I'd group the elevators so some only go to high floors and others only to low floors. I'd also focus heavily on clear buttons and emergency safety measures.", "keywords": ["reducing wait times", "group", "high floors", "clear buttons", "safety measures"]},
        ]
    },
    "Frontend Developer": {
        "Technical": [
            {"q": "What is the virtual DOM and how does React use it?", "ideal": "The virtual DOM is a lightweight copy of the web page kept in memory. When something changes, React updates this copy first, finds out exactly what the differences are, and then changes only those specific tiny parts on the real screen. This makes apps feel very fast.", "keywords": ["copy", "memory", "differences", "specific parts", "real screen", "fast"]},
            {"q": "Explain semantic HTML and why it is important.", "ideal": "Semantic HTML means using the correct tags for the job, like using a <nav> tag for a navigation bar instead of a generic <div>. This matters heavily because it helps blind users with screen readers understand the page, and helps Google index the site better.", "keywords": ["correct tags", "nav", "div", "screen readers", "Google index", "understand"]},
            {"q": "How do you optimize the performance of a web application?", "ideal": "I focus on making things smaller and faster. I compress images, break my code into smaller pieces so it only loads what's needed right now, and use caching so users don't have to re-download the same files twice. Keeping the site snappy is the main priority.", "keywords": ["smaller", "faster", "compress", "code into pieces", "caching", "snappy"]},
        ],
        "Behavioral": [
            {"q": "How do you balance design requirements with technical constraints?", "ideal": "I treat designers as partners. If an animation is going to make the site unacceptably slow, I'll explain the performance trade-off to them and suggest a slightly simpler, faster alternative that still looks incredibly good and meets the user goal.", "keywords": ["partners", "slow", "performance trade-off", "simpler", "alternative", "looks good"]},
        ],
        "System Design": [
            {"q": "How would you architect a scalable frontend application?", "ideal": "I would build it using small, reusable components so we aren't writing the same code twice. I'd keep the app's overall state centralized and organized, and ensure there’s a solid automated testing system so that new updates don't accidentally break old features.", "keywords": ["reusable components", "centralized state", "organized", "testing system", "break old features"]},
        ]
    },
    "Backend Developer": {
        "Technical": [
            {"q": "What are the advantages of microservices over a monolithic architecture?", "ideal": "A monolith is one giant block of code, while microservices act like separate, small apps that talk to each other. The advantage of microservices is that a crash in one small part doesn't take down the entire website, and different teams can work without stepping on toes.", "keywords": ["giant block", "separate", "crash", "take down", "different teams"]},
            {"q": "Explain ACID properties in databases.", "ideal": "ACID is a set of rules ensuring database transactions are safe. Basically, it promises that an operation either finishes completely or fails completely (Atomicity), the data stays valid (Consistency), multiple user transactions don't mess each other up (Isolation), and saved data doesn't get lost when the power goes out (Durability).", "keywords": ["safe", "finishes completely", "fails completely", "valid", "mess each other up", "power goes out"]},
            {"q": "How do you prevent SQL injection?", "ideal": "SQL injection is when hackers sneak malicious commands into text boxes. I prevent it primarily by using 'parameterized queries,' which forces the database to treat what the user typed strictly as normal text, not as an executable command.", "keywords": ["hackers", "text boxes", "parameterized queries", "normal text", "executable"]},
        ],
        "System Design": [
            {"q": "Design an API for a simple e-commerce checkout.", "ideal": "I'd design clear, secure endpoints for adding to the cart and handling payments. The most important piece is making the payment endpoint safe and 'idempotent'—meaning if a customer accidentally clicks 'Buy' twice because of lag, they are only charged once.", "keywords": ["secure endpoints", "handling payments", "idempotent", "clicks 'Buy'", "charged once"]},
        ]
    },
    "UI/UX Designer": {
        "Technical": [
            {"q": "Explain your design process from concept to handoff.", "ideal": "I start by talking to users to understand what they need. Then, I quickly sketch out wireframes. Once the team likes the basic flow, I create the polished, colorful designs. Finally, I test it with real users and hand off neatly organized files to the developers.", "keywords": ["talking to users", "wireframes", "flow", "colorful designs", "test", "organized files"]},
            {"q": "What is the difference between UI and UX?", "ideal": "UX (User Experience) is how the product feels and works; it's the logic and the journey you take. UI (User Interface) is how it looks; it includes the colors, buttons, fonts, and the actual visual polish on the screen.", "keywords": ["feels and works", "logic", "journey", "looks", "colors", "visual polish"]},
        ],
        "Behavioral": [
            {"q": "How do you handle negative feedback on a design?", "ideal": "I remind myself that the feedback is about the work, not me personally. Instead of getting defensive, I ask questions to understand why it isn't working for them. I rely heavily on user testing data to guide the next round of improvements.", "keywords": ["about the work", "defensive", "understand why", "user testing data", "improvements"]},
        ]
    },
    "DevOps Engineer": {
        "Technical": [
            {"q": "What is Infrastructure as Code (IaC)?", "ideal": "Instead of clicking buttons in a cloud console to create servers, IaC means we write computer code to define what our servers should look like. This guarantees that our setups are consistent, perfectly reproducible, and easily stored in version control.", "keywords": ["clicking buttons", "computer code", "consistent", "reproducible", "version control"]},
            {"q": "Explain Blue-Green deployments vs Canary releases.", "ideal": "Blue-Green uses an identical, parallel environment to switch everyone over instantly with zero downtime. Canary releases are much more cautious: we slowly give the update to 5% of our users, check for errors, and quietly roll it out to the rest if everything looks great.", "keywords": ["parallel environment", "zero downtime", "cautious", "5%", "errors", "roll it out"]},
        ],
        "System Design": [
            {"q": "How would you design a CI/CD pipeline for a microservices app?", "ideal": "When a developer pushes code, the pipeline should automatically run tests to ensure nothing broke. Then, it places the code cleanly inside a Docker container, does a quick security scan, and uses tools like Kubernetes to seamlessly update the live application.", "keywords": ["automatically", "tests", "Docker container", "security scan", "Kubernetes", "update"]},
        ]
    },
    "Full Stack Developer": {
        "Technical": [
            {"q": "How do you handle state management across the frontend and backend?", "ideal": "On the frontend, I keep track of what the user is currently doing using React state or Redux. On the backend, permanent data is carefully stored in a true database. The two sides stay perfectly in sync by talking to each other using well-structured APIs.", "keywords": ["currently doing", "React state", "permanent data", "database", "in sync", "APIs"]},
            {"q": "Explain Cross-Origin Resource Sharing (CORS).", "ideal": "CORS is a security feature built into web browsers. It naturally stops an evil website from sneakily requesting data from your bank's API. A server has to explicitly list out which websites are safely allowed to talk to it.", "keywords": ["security feature", "evil website", "bank's API", "explicitly", "safely allowed"]},
        ],
        "System Design": [
            {"q": "Design a real-time chat application.", "ideal": "I'd use WebSockets so messages appear instantly without needing to refresh the page. I'd back that up with a fast messaging queue and a modern NoSQL database that can easily handle extremely fast, frequent reads and writes.", "keywords": ["WebSockets", "instantly", "refresh", "queue", "NoSQL database", "frequent", "writes"]},
        ],
        "Case Study": [
            {"q": "How would you optimize a slow-loading web application?", "ideal": "I would use browser tools to spot exactly what is dragging it down. On the front end, I'd shrink image sizes and delay loading parts of the page that aren't on screen. On the backend, I'd make sure database queries are heavily optimized and cached.", "keywords": ["browser tools", "dragging it down", "shrink", "delay loading", "queries", "cached"]},
        ]
    },
    "Cloud Engineer": {
        "Technical": [
            {"q": "What are the core differences between IaaS, PaaS, and SaaS?", "ideal": "IaaS is renting basic computers and networks in the cloud. PaaS gives you a ready-made platform so you only worry about deploying code, skipping the server headaches. SaaS is just a fully finished app that you log into and use, like Gmail.", "keywords": ["renting basic computers", "ready-made platform", "deploying code", "server headaches", "fully finished", "log into"]},
            {"q": "Explain the concept of Auto Scaling.", "ideal": "Auto Scaling keeps an eye on your tech traffic. If your website suddenly goes viral and traffic spikes, it automatically creates fresh new servers to handle the load. When it gets quiet again, it automatically shuts them down to save a ton of money.", "keywords": ["traffic", "spikes", "automatically creates", "handle the load", "shuts them down", "save money"]},
        ],
        "System Design": [
            {"q": "How would you design a highly available architecture on AWS?", "ideal": "I would avoid putting all my eggs in one basket by spreading my servers securely across multiple physical data centers (Availability Zones). I'd put a smart load balancer right in front to steer traffic safely away from any servers that act up.", "keywords": ["eggs in one basket", "spreading", "data centers", "load balancer", "steer traffic", "act up"]},
        ]
    },
    "Machine Learning Engineer": {
        "Technical": [
            {"q": "Describe the architecture of a Transformer model.", "ideal": "Transformers process large amounts of text by paying 'attention' to all the words at the same time to really understand the deep context, rather than strictly reading one word after the other. This makes them incredibly powerful for understanding human language.", "keywords": ["process large amounts", "attention", "all the words", "context", "human language"]},
            {"q": "How do you deploy an ML model to production?", "ideal": "I wrap the finished model inside an API so other apps can easily ask it questions. I package it all neatly within a robust Docker container so it works perfectly anywhere, and set up clear monitoring to catch if the model starts giving noticeably bad answers later.", "keywords": ["wrap", "API", "package", "Docker container", "monitoring", "bad answers"]},
        ],
        "Behavioral": [
             {"q": "Tell me about a time a model failed in production.", "ideal": "I would openly discuss a case where the live model's accuracy dropped because real-world trends changed. I caught it quickly using solid monitoring graphs, retrained the model on newer data, and created a totally automated system to prevent it going stale again.", "keywords": ["accuracy dropped", "real-world trends", "monitoring graphs", "retrained", "automated system", "stale"]},
        ],
        "Case Study": [
             {"q": "How would you design a recommendation system for an e-commerce platform?", "ideal": "I would rely on a mix of two things: what the specific user has liked in the past, and what similar buyers highly loved. To make it extremely fast, I'd use an optimized search index to instantly grab the top 100 choices before smoothly predicting the absolute best match.", "keywords": ["liked in the past", "similar buyers", "extremely fast", "search index", "predicting", "absolute best match"]},
        ]
    },
    "Cybersecurity Analyst": {
        "Technical": [
            {"q": "What is the difference between symmetric and asymmetric encryption?", "ideal": "Symmetric encryption uses only one single secret key to accurately lock and unlock a message, which is super fast but tricky to share. Asymmetric uses two keys—a public one to lock the message, and a securely hidden private one to unlock it.", "keywords": ["one single secret key", "lock and unlock", "tricky to share", "two keys", "public", "private"]},
            {"q": "Explain what a Man-in-the-Middle (MitM) attack is and how to prevent it.", "ideal": "It's when an attacker sits quietly between you and a website, secretly reading or changing your valuable data. We absolutely prevent it by always forcing strongly encrypted connections (like HTTPS) so the attacker only ever sees meaningless garbage.", "keywords": ["sits quietly", "secretly reading", "valuable data", "encrypted connections", "HTTPS", "garbage"]},
        ],
        "Behavioral": [
            {"q": "How do you stay updated with the latest security threats?", "ideal": "Hackers move surprisingly quickly, so I stay highly active. I read industry tech blogs, follow official threat alerts heavily, and regularly practice identifying issues in secure, ethical hacking environments to keep my hands-on skills sharp.", "keywords": ["hacker", "blogs", "threat alerts", "practice", "ethical hacking", "hands-on skills"]},
        ]
    },
    "Database Administrator": {
         "Technical": [
            {"q": "What is normalization and why is it important?", "ideal": "Normalization is organizing your database perfectly to eliminate wasteful duplicate data. Instead of typing out a company's address 500 times for every employee, you put the address safely in one spot and reliably link to it, keeping the data super safe and consistent.", "keywords": ["organizing", "eliminate wasteful", "duplicate", "one spot", "link", "safe and consistent"]},
            {"q": "Explain the difference between clustered and non-clustered indexes.", "ideal": "A clustered index literally decides the exact physical order the data is written on the hard drive, so you only get one per table. A non-clustered index acts strictly like the index at the back of a textbook: it’s a tiny separate list that quickly points to where the real data is.", "keywords": ["physical order", "hard drive", "one per table", "back of a textbook", "separate list", "points"]},
        ],
        "Case Study": [
            {"q": "How would you troubleshoot a slow database querying system?", "ideal": "I would directly ask the database software to explain step-by-step how it is finding the answer. Often, adding a simple missing index acts as a shortcut that instantly speeds things up. I'd also check if the server is simply running entirely out of fresh memory.", "keywords": ["explain step-by-step", "finding the answer", "missing index", "shortcut", "speeds things up", "memory"]},
        ]
    },
    "Mobile App Developer": {
        "Technical": [
            {"q": "Explain the application lifecycle in iOS or Android.", "ideal": "An app neatly loops through phases: it opens (active), gets minimized to the background to handle text messages (inactive/background), and eventually gets force-closed. Good code handles these perfectly so you easily keep your spot and don't rapidly drain the user's precious battery.", "keywords": ["active", "background", "force-closed", "keep your spot", "drain", "battery"]},
            {"q": "How do you manage memory limits in a mobile application?", "ideal": "Phones have strictly limited memory, so I am very careful to immediately clean out large things, like giant high-res images, from memory as soon as they scroll off-screen. I ensure the code doesn't hold tightly onto data it genuinely no longer needs.", "keywords": ["strictly limited memory", "careful", "clean out", "scroll off-screen", "hold tightly", "no longer needs"]},
        ],
         "Case Study": [
             {"q": "Design the architecture for an offline-first mobile app.", "ideal": "I would store all the user interaction directly in a secure local database firmly on the phone so the app responds instantly. When the phone finally gets cell service back, it smoothly and quietly syncs all those changes accurately with the remote main server in the background.", "keywords": ["secure local database", "instantly", "cell service back", "smoothly and quietly", "syncs", "background"]},
         ]
    },
    "QA Automation Engineer": {
        "Technical": [
            {"q": "What is the Page Object Model (POM) and why use it?", "ideal": "POM is an exceptionally smart way to organize tests. Instead of tossing raw clicks directly into the test code, you map out the buttons on a beautifully centralized 'Page' file. When developers totally change a button, you smartly fix it in just one single place.", "keywords": ["smart way", "tossing raw clicks", "map out", "centralized", "fix it", "one single place"]},
            {"q": "Explain the difference between Smoke, Sanity, and Regression testing.", "ideal": "Smoke testing broadly ensures the app literally turns on without crashing. Sanity testing deeply double-checks a specific tiny bug fix. Regression testing thoroughly runs absolutely everything to ensure your incredibly sparkling new changes didn't accidentally break old features.", "keywords": ["turns on", "crashing", "tiny bug fix", "runs absolutely everything", "sparkling new", "break old features"]},
        ],
        "System Design": [
             {"q": "How would you design a test automation framework from scratch?", "ideal": "I would cleanly build it using stable, popular tools, keeping the test data intentionally separated from the test scripts. I'd strongly connect the framework into our daily pipeline so tests run fully automatically on every single developer update, stopping bad code entirely.", "keywords": ["stable", "test data", "separated", "daily pipeline", "fully automatically", "stopping bad code"]},
        ]
    }
}

basic_questions = [
    {"q": "Tell me about yourself.", "ideal": "Keep it very professional and focused heavily on your work history. Quickly highlight a few highly relevant past experiences, talk briefly about what you are currently doing, and smoothly end by showing why connecting with their specific company excites you.", "keywords": ["professional", "work history", "relevant", "currently doing", "company excites"]},
    {"q": "What are your greatest strengths?", "ideal": "Name one or two very solid skills (like quick adaptability or excellent communication) and firmly back them up with a short, powerful story. Showing exactly *how* you used the strength in reality is always way better than simply stating words.", "keywords": ["one or two", "adaptability", "communication", "powerful story", "how you used"]},
    {"q": "What is your greatest weakness?", "ideal": "Honestly share a minor, completely understandable flaw that doesn't inherently ruin the job requirements—like occasionally taking on too much work. The critical secret is to strongly emphasize the exact, smart steps you are proactively taking to reliably improve on it right now.", "keywords": ["minor flaw", "understandable", "taking on too much", "critical secret", "improve", "right now"]},
    {"q": "Where do you see yourself in five years?", "ideal": "Show genuine ambition that tightly aligns with the team's goals. Express a confident desire to heavily deepen your core skills, confidently take on more serious responsibility, and consistently deliver massive positive value directly to the company.", "keywords": ["ambition", "team's goals", "deepen skills", "responsibility", "positive value", "company"]},
    {"q": "Describe a difficult work situation and how you overcame it.", "ideal": "Use a clear story to prove you stay perfectly calm. Quickly outline the challenging problem, clearly explain the logical, level-headed steps you personally took to boldly solve it, and loudly highlight the hugely successful outcome.", "keywords": ["clear story", "stay perfectly calm", "challenging problem", "logical steps", "boldly solve", "successful outcome"]},
    {"q": "Why do you want to work here?", "ideal": "Honestly explain what strongly attracts you to their exact product, their very specific company culture, or the unique tech stack they use. This explicitly proves you confidently did your homework and aren't just desperately applying truly anywhere.", "keywords": ["strongly attracts", "exact product", "company culture", "unique tech stack", "did your homework", "desperately applying"]},
    {"q": "Why should we hire you?", "ideal": "Confidently summarize exactly how your specific, highly unique past experiences directly match the incredibly important pain points mentioned in their exact job description. Provide absolute assurance that you can very easily step right in and instantly solve their problems.", "keywords": ["summarize", "unique past experiences", "match", "pain points", "job description", "step right in", "solve their problems"]},
    {"q": "What is your greatest professional achievement?", "ideal": "Proudly share a major project where your direct involvement genuinely mattered. Heavily emphasize the concrete, undeniable metrics—like significantly saving the team precious time or vastly increasing user revenue—so they easily understand your true, massive impact.", "keywords": ["major project", "involvement mattered", "metrics", "saving time", "user revenue", "massive impact"]},
    {"q": "Tell me about a time you failed.", "ideal": "Be incredibly honest about a true, unmistakable mistake you confidently made. Employers massively appreciate candidates who can bravely own a negative outcome, swiftly analyze precisely what definitely went wrong, and completely change their incredibly safe processes to securely ensure it never forcefully happens again.", "keywords": ["incredibly honest", "mistake", "own a negative outcome", "analyze", "went wrong", "change processes", "never happens again"]},
    {"q": "How do you handle stress and pressure?", "ideal": "Explain your very practical methods for calmly maintaining top-level focus. Discuss how you strategically slice massive, incredibly overwhelming major projects into tiny, very manageable daily tasks, strongly relying on crystal-clear communication strictly with your team.", "keywords": ["practical methods", "focus", "slice massive projects", "manageable daily tasks", "crystal-clear communication"]},
    {"q": "What are your salary expectations?", "ideal": "Politely indicate that you confidently did heavy research to deeply understand the fair market rates. Offer a highly reasonable range, clearly noting that you fundamentally value the incredible entire compensation package heavily over just the sheer base salary number.", "keywords": ["heavy research", "understand", "fair market rates", "reasonable range", "value", "compensation package", "base salary"]},
    {"q": "What do you like to do outside of work?", "ideal": "Briefly share a cool, harmless hobby that humanizes you cleanly. It heavily shows you are a totally balanced person securely capable of gracefully avoiding total burnout. Extra massive bonus points if your hobby shows incredible creativity or serious teamwork.", "keywords": ["harmless hobby", "humanizes", "balanced person", "avoiding burnout", "bonus points", "creativity", "teamwork"]},
    {"q": "How do you prioritize your work?", "ideal": "Describe a surprisingly simple framework for successfully determining the extreme true urgency heavily relative to the overall important business impact. Show exactly how you smoothly adapt on the absolute fly when incredibly major emergencies suddenly strongly pop up.", "keywords": ["framework", "extreme true urgency", "business impact", "smoothly adapt", "absolute fly", "major emergencies"]},
    {"q": "What is your ideal work environment?", "ideal": "Describe an energetic place heavily driven securely by mutual, incredible trust and perfectly open communication, rather than exhausting extreme micromanagement. Highlight exactly how you firmly thrive when totally empowered to take absolute, incredible ownership of your unique work.", "keywords": ["mutual trust", "open communication", "micromanagement", "thrive", "empowered", "ownership"]},
    {"q": "What coding language are you most comfortable with?", "ideal": "Confidently name your primary, incredibly strongest language perfectly while firmly emphasizing that a programming language is essentially just a highly useful tool. Seriously stress how powerfully, amazingly fast you can readily fiercely adapt to incredibly new, absolutely required technology frameworks.", "keywords": ["strongest language", "useful tool", "fast", "fiercely adapt", "new", "technology frameworks"]}
]

for role in existing_db:
    existing_db[role]["Basic"] = basic_questions

with open("questions.py", "w") as f:
    f.write("QUESTIONS_DB = " + json.dumps(existing_db, indent=4))
