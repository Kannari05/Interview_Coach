import json

existing_db = {
    "Software Engineer": {
        "Technical": [
            {"q": "Explain the difference between a stack and a queue.", "ideal": "A stack follows LIFO (Last In First Out) where elements are added and removed from the top. A queue follows FIFO (First In First Out) where elements are added at the back and removed from the front. Stacks are used in recursion and undo operations; queues in scheduling and BFS.", "keywords": ["LIFO", "FIFO", "stack", "queue", "recursion", "scheduling"]},
            {"q": "What is the time complexity of binary search?", "ideal": "Binary search has O(log n) time complexity because it halves the search space at each step. It requires the array to be sorted. Space complexity is O(1) for iterative and O(log n) for recursive implementations.", "keywords": ["O(log n)", "sorted", "halves", "binary", "iterative", "recursive"]},
            {"q": "Describe RESTful API principles.", "ideal": "REST stands for Representational State Transfer. Principles include statelessness, client-server architecture, uniform interface, cacheability, layered system, and code on demand. HTTP methods GET, POST, PUT, DELETE map to CRUD operations.", "keywords": ["stateless", "client-server", "HTTP", "GET", "POST", "CRUD", "uniform"]},
            {"q": "How does garbage collection work in Java or Python?", "ideal": "In Python, it uses reference counting and a cyclic garbage collector. In Java, it happens in the JVM where unused objects in the heap are automatically deleted. Generational garbage collection focuses on short-lived objects.", "keywords": ["reference counting", "cyclic", "JVM", "heap", "Generational"]},
            {"q": "What is the difference between an abstract class and an interface?", "ideal": "An abstract class can have method implementations and state variables, but cannot be instantiated. An interface only defines method signatures (though modern languages allow default methods) and allows multiple inheritance.", "keywords": ["instantiated", "method signatures", "multiple inheritance", "state variables"]},
        ],
        "Behavioral": [
            {"q": "Tell me about a time you debugged a critical production issue.", "ideal": "Use the STAR method: describe the Situation, your Task, the Actions you took (isolating logs, reproducing, rolling back, fixing), and the Result. Mention communication with team and stakeholders.", "keywords": ["logs", "reproduce", "rollback", "fix", "team", "communication", "STAR"]},
            {"q": "How do you handle disagreements with teammates on technical decisions?", "ideal": "I listen actively, present data-driven arguments, look for common ground, and escalate when needed. I separate technical merit from personal preference and prioritize team cohesion.", "keywords": ["listen", "data", "evidence", "compromise", "escalate", "respect"]},
            {"q": "Describe a time when you had to learn a new technology quickly.", "ideal": "I started with the official documentation and built a small proof of concept. I also looked at community examples and asked experienced teammates for code reviews to validate my understanding.", "keywords": ["documentation", "proof of concept", "community", "code reviews", "validate"]},
        ],
        "System Design": [
            {"q": "Design a URL shortening service like bit.ly.", "ideal": "Cover: hashing strategy (MD5/base62), database choice (NoSQL for scale), cache layer (Redis), load balancer, expiry TTL, analytics, rate limiting, and handling collisions.", "keywords": ["hash", "base62", "database", "cache", "Redis", "load balancer", "collision"]},
            {"q": "How would you design a rate limiter?", "ideal": "Use algorithms like Token Bucket, Leaky Bucket, or Sliding Window. Implement logic using a distributed cache like Redis to store counters, and define limits based on IP or user ID.", "keywords": ["Token Bucket", "Sliding Window", "Redis", "counters", "distributed cache"]},
        ]
    },
    "Data Scientist": {
        "Technical": [
            {"q": "Explain overfitting and how to prevent it.", "ideal": "Overfitting occurs when a model learns noise in training data and performs poorly on unseen data. Prevention: regularization (L1/L2), dropout, cross-validation, early stopping, more training data, simpler model architecture.", "keywords": ["overfitting", "regularization", "L1", "L2", "cross-validation", "dropout", "generalization"]},
            {"q": "What is the difference between bagging and boosting?", "ideal": "Bagging builds models in parallel on bootstrap samples and averages results (e.g., Random Forest). Boosting builds models sequentially, each correcting the previous (e.g., XGBoost, AdaBoost). Bagging reduces variance; boosting reduces bias.", "keywords": ["bagging", "boosting", "parallel", "sequential", "Random Forest", "XGBoost", "variance", "bias"]},
            {"q": "How do you handle missing or corrupted data in a dataset?", "ideal": "I first analyze the pattern of missingness. Then I can drop columns/rows with too many missing values, or impute them using mean/median/mode, or use predictive imputation techniques like KNN.", "keywords": ["missingness", "drop", "impute", "mean", "median", "KNN"]},
        ],
        "Behavioral": [
            {"q": "Describe a project where your model had unexpected results.", "ideal": "Explain the project goal, what unexpected results appeared, root cause analysis (data leakage, distribution shift, wrong metric), and corrective actions taken. Emphasize learning and documentation.", "keywords": ["unexpected", "root cause", "data leakage", "distribution", "metric", "corrective", "learning"]},
            {"q": "How do you explain complex technical concepts to non-technical stakeholders?", "ideal": "I avoid jargon, use analogies, and focus on the business impact. Visualizations and clear dashboards help illustrate the story the data is telling without getting bogged down in math.", "keywords": ["jargon", "analogies", "business impact", "visualizations", "dashboards", "story"]},
        ],
        "Case Study": [
            {"q": "How would you build a churn prediction model?", "ideal": "Define churn, gather features (usage frequency, tenure, billing), handle imbalanced data (SMOTE, class weights), try logistic regression and gradient boosting, evaluate with AUC-ROC and precision-recall, deploy with monitoring.", "keywords": ["churn", "features", "imbalanced", "SMOTE", "AUC", "precision", "recall", "gradient boosting"]},
        ]
    },
    "Product Manager": {
        "Behavioral": [
            {"q": "Tell me about a product you shipped from idea to launch.", "ideal": "Walk through discovery (user research, problem validation), prioritization (RICE/MoSCoW), roadmap, collaboration with engineering/design, launch strategy, and post-launch metrics tracking.", "keywords": ["research", "validation", "prioritization", "roadmap", "launch", "metrics", "stakeholders"]},
            {"q": "How do you prioritize features when everything seems urgent?", "ideal": "I use frameworks like RICE (Reach, Impact, Confidence, Effort) or MoSCoW. I align with business OKRs, gather data on user impact, and facilitate stakeholder alignment sessions.", "keywords": ["RICE", "MoSCoW", "OKR", "prioritize", "data", "stakeholders", "impact"]},
            {"q": "Describe a time when a product launch failed. What did you learn?", "ideal": "I would structure the answer by explaining the context, the exact cause of the failure (e.g., poor marketing, technical flaw, ignored user feedback), the immediate reaction to fix it, and the retrospective lessons learned.", "keywords": ["context", "cause", "user feedback", "fix", "retrospective", "lessons learned"]},
        ],
        "Case Study": [
            {"q": "How would you improve our mobile app's user retention?", "ideal": "Define retention metrics, segment users by cohort, identify drop-off points via funnel analysis, run A/B tests on onboarding, push notifications, and feature discovery. Measure with 30/60/90-day retention.", "keywords": ["retention", "cohort", "funnel", "A/B test", "onboarding", "notifications", "metrics"]},
            {"q": "Design an elevator system for a 100-story building.", "ideal": "Identify user personas and pain points, set goals (minimize wait time, maximize throughput). Discuss zoning, peak hours logic, emergency modes, and key metrics like average wait time.", "keywords": ["personas", "pain points", "goals", "zoning", "peak hours", "metrics", "wait time"]},
        ]
    },
    "Frontend Developer": {
        "Technical": [
            {"q": "What is the virtual DOM and how does React use it?", "ideal": "The virtual DOM is a lightweight JavaScript representation of the actual DOM. React compares the new virtual DOM with a snapshot of the old one (diffing) to calculate the minimal number of DOM patches required, optimizing performance.", "keywords": ["virtual DOM", "representation", "snapshot", "diffing", "patches", "optimizing"]},
            {"q": "Explain semantic HTML and why it is important.", "ideal": "Semantic HTML uses tags that convey the meaning of the content (like article, nav, header). It improves accessibility for screen readers and helps with SEO, making the page easier to navigate.", "keywords": ["convey meaning", "article", "nav", "accessibility", "screen readers", "SEO"]},
            {"q": "How do you optimize the performance of a web application?", "ideal": "We can optimize via code splitting, lazy loading images and components, minifying CSS/JS, using CDNs, caching, reducing DOM elements, and optimizing Web Vitals (LCP, FID, CLS).", "keywords": ["code splitting", "lazy loading", "minifying", "CDN", "caching", "Web Vitals"]},
        ],
        "Behavioral": [
            {"q": "How do you balance design requirements with technical constraints?", "ideal": "I collaborate closely with designers early in the process to discuss technical feasibility. We negotiate compromises that preserve the user experience while staying within performance or framework limits.", "keywords": ["collaborate", "designers", "feasibility", "compromises", "user experience", "performance"]},
        ],
        "System Design": [
            {"q": "How would you architect a scalable frontend application?", "ideal": "Use component-driven architecture, a global state management tool (like Redux or Context API), a design system with reusable UI components, strict linting/formatting rules, and implement a robust CI/CD pipeline.", "keywords": ["component-driven", "state management", "design system", "reusable", "CI/CD"]},
        ]
    },
    "Backend Developer": {
        "Technical": [
            {"q": "What are the advantages of microservices over a monolithic architecture?", "ideal": "Microservices offer independent deployment, specialized technology stacks, fault isolation, and easier scaling of specific components. However, they introduce complexity in networking and data consistency.", "keywords": ["independent deployment", "fault isolation", "scaling", "complexity", "networking", "consistency"]},
            {"q": "Explain ACID properties in databases.", "ideal": "ACID stands for Atomicity (all or nothing), Consistency (valid state transitions), Isolation (concurrent transactions don't interfere), and Durability (committed data is saved safely).", "keywords": ["Atomicity", "Consistency", "Isolation", "Durability", "transactions", "valid state"]},
            {"q": "How do you prevent SQL injection?", "ideal": "I prevent SQL injection by using parameterized queries or prepared statements, validating and sanitizing user input, using ORM libraries, and enforcing least privilege at the database level.", "keywords": ["parameterized", "prepared statements", "sanitizing", "ORM", "least privilege"]},
        ],
        "System Design": [
            {"q": "Design an API for a simple e-commerce checkout.", "ideal": "Include endpoints for adding to cart, applying discounts, and submitting payment. Discuss idempotency for payment APIs, handling inventory locks, and eventual consistency for order processing.", "keywords": ["endpoints", "idempotency", "inventory locks", "eventual consistency", "payment"]},
        ]
    },
    "UI/UX Designer": {
        "Technical": [
            {"q": "Explain your design process from concept to handoff.", "ideal": "I start with user research and identifying personas, then create wireframes and user flows. After low-fidelity prototypes, I move to high-fidelity designs, conduct usability testing, and finally hand off assets via Figma to developers.", "keywords": ["user research", "personas", "wireframes", "prototypes", "usability testing", "handoff"]},
            {"q": "What is the difference between UI and UX?", "ideal": "UX (User Experience) is about the journey, logic, and how a product feels or works for the user. UI (User Interface) focuses on the visual touchpoints, like typography, colors, padding, and layout.", "keywords": ["journey", "logic", "feels", "visual", "typography", "layout"]},
        ],
        "Behavioral": [
            {"q": "How do you handle negative feedback on a design?", "ideal": "I don't take it personally. I ask clarifying questions to understand the root of the feedback, check if the criticism aligns with user goals, and iterate on the design using data-backed decisions.", "keywords": ["personally", "clarifying", "root", "user goals", "iterate", "data-backed"]},
        ]
    },
    "DevOps Engineer": {
        "Technical": [
            {"q": "What is Infrastructure as Code (IaC)?", "ideal": "IaC is managing and provisioning computing infrastructure through machine-readable definition files, rather than physical hardware configuration. Tools include Terraform, Ansible, and CloudFormation.", "keywords": ["managing", "provisioning", "definition files", "Terraform", "Ansible", "CloudFormation"]},
            {"q": "Explain Blue-Green deployments vs Canary releases.", "ideal": "Blue-Green uses two identical environments to switch traffic instantly, allowing fast rollbacks. Canary gradually rolls out changes to a small subset of users to monitor for errors before full deployment.", "keywords": ["identical environments", "switch traffic", "rollbacks", "gradually", "subset", "monitor"]},
        ],
        "System Design": [
            {"q": "How would you design a CI/CD pipeline for a microservices app?", "ideal": "I'd use a version control system triggered webhook, automated unit and integration tests, Docker image building, pushing to a registry, and deploying via Kubernetes/Helm. Include security scanning and notifications.", "keywords": ["webhook", "automated tests", "Docker", "registry", "Kubernetes", "security scanning"]},
        ]
    },
    "Full Stack Developer": {
        "Technical": [
            {"q": "How do you handle state management across the frontend and backend?", "ideal": "On the frontend, I use tools like Redux or React Context. On the backend, state is stored persistently in databases or caches like Redis. I ensure synchronization via REST or GraphQL APIs and WebSockets for real-time updates.", "keywords": ["Redux", "Context", "databases", "Redis", "synchronization", "REST", "GraphQL", "WebSockets"]},
            {"q": "Explain Cross-Origin Resource Sharing (CORS).", "ideal": "CORS is a security feature implemented by browsers that blocks web pages from making requests to a different domain than the one that served the web page. It is configured on the server via HTTP headers to allow specific origins.", "keywords": ["security", "browsers", "domain", "server", "HTTP headers", "origins"]}
        ],
        "System Design": [
            {"q": "Design a real-time chat application.", "ideal": "I would use WebSockets for real-time bi-directional communication, a backend managed by Node.js or Go, and a NoSQL database like MongoDB or Cassandra for fast read/writes. I'd add a cache layer like Redis for user presence and message queuing.", "keywords": ["WebSockets", "Node.js", "NoSQL", "MongoDB", "Redis", "presence", "queuing"]}
        ],
        "Case Study": [
            {"q": "How would you optimize a slow-loading web application?", "ideal": "I would profile the app using Chrome DevTools. Frontend optimizations include lazy loading, code splitting, minimizing bundle size, and optimizing images. Backend optimizations include database indexing, query optimization, and implementing API caching.", "keywords": ["profile", "DevTools", "lazy loading", "code splitting", "indexing", "caching"]}
        ]
    },
    "Cloud Engineer": {
        "Technical": [
            {"q": "What are the core differences between IaaS, PaaS, and SaaS?", "ideal": "IaaS provides raw computing resources like VMs and networks (e.g., AWS EC2). PaaS provides a platform allowing customers to develop and manage apps without infrastructure logic (e.g., Heroku). SaaS delivers software over the internet (e.g., Google Workspace).", "keywords": ["computing resources", "VMs", "platform", "infrastructure", "software", "internet"]},
            {"q": "Explain the concept of Auto Scaling.", "ideal": "Auto Scaling monitors applications and automatically adjusts capacity to maintain steady, predictable performance at the lowest possible cost. It dynamically adds or removes compute instances based on metrics like CPU utilization or network traffic.", "keywords": ["monitors", "capacity", "cost", "dynamically", "instances", "metrics", "CPU"]}
        ],
        "System Design": [
            {"q": "How would you design a highly available architecture on AWS?", "ideal": "I would distribute resources across multiple Availability Zones (AZs) using Application Load Balancers. I'd use Auto Scaling Groups for EC2 instances, a multi-AZ RDS setup for the database, and Route 53 for DNS failover routing.", "keywords": ["distribute", "Availability Zones", "Load Balancers", "Auto Scaling", "multi-AZ", "Route 53", "failover"]}
        ]
    },
    "Machine Learning Engineer": {
        "Technical": [
            {"q": "Describe the architecture of a Transformer model.", "ideal": "Transformers rely entirely on self-attention mechanisms to compute representations of inputs and outputs without sequence-aligned RNNs or convolutions. Key components include multi-head attention, feed-forward networks, and positional encoding.", "keywords": ["self-attention", "sequence-aligned", "multi-head", "feed-forward", "positional encoding"]},
            {"q": "How do you deploy an ML model to production?", "ideal": "I containerize the model using Docker and deploy it via an API framework like FastAPI. For large scale, I use orchestration tools like Kubernetes or serverless options like AWS SageMaker, ensuring we monitor for model drift post-deployment.", "keywords": ["containerize", "Docker", "API", "FastAPI", "Kubernetes", "SageMaker", "model drift"]}
        ],
        "Behavioral": [
             {"q": "Tell me about a time a model failed in production.", "ideal": "Once a model suffered from concept drift as user behavior changed post-launch. I identified the performance drop through monitoring dashboards, retrained the model on recent data, and implemented a pipeline for automated periodic retraining.", "keywords": ["concept drift", "monitoring", "dashboards", "retrained", "pipeline", "automated"]}
        ],
        "Case Study": [
             {"q": "How would you design a recommendation system for an e-commerce platform?", "ideal": "I'd start with a hybrid approach combining collaborative filtering (user-item matrix factorization) and content-based filtering (item metadata). I'd retrieve candidates fast using approximate nearest neighbors (FAISS) and rank them using an advanced model like XGBoost or a deep neural net.", "keywords": ["hybrid", "collaborative filtering", "content-based", "matrix factorization", "candidates", "nearest neighbors", "FAISS", "rank"]}
        ]
    },
    "Cybersecurity Analyst": {
        "Technical": [
            {"q": "What is the difference between symmetric and asymmetric encryption?", "ideal": "Symmetric encryption uses a single key for both encryption and decryption, making it faster but harder to share securely. Asymmetric uses a pair of keys (public and private), providing better security for key exchange but is slower.", "keywords": ["single key", "encryption", "decryption", "pair", "public", "private", "exchange"]},
            {"q": "Explain what a Man-in-the-Middle (MitM) attack is and how to prevent it.", "ideal": "A MitM attack intercepts communication between two parties to steal or alter data. Prevention involves strong encryption like HTTPS/TLS, secure VPNs, certificate pinning, and avoiding public Wi-Fi without protective measures.", "keywords": ["intercepts", "steal", "alter", "HTTPS", "TLS", "VPNs", "certificate pinning"]}
        ],
        "Behavioral": [
            {"q": "How do you stay updated with the latest security threats?", "ideal": "I regularly read security blogs, follow CVE databases, participate in forums like Reddit Netsec, and subscribe to alerts from organizations like CISA. I also engage in ethical hacking labs like HackTheBox to practice.", "keywords": ["blogs", "CVE", "forums", "Netsec", "CISA", "ethical hacking", "HackTheBox"]}
        ]
    },
    "Database Administrator": {
         "Technical": [
            {"q": "What is normalization and why is it important?", "ideal": "Normalization is the process of organizing data in a database to reduce redundancy and improve data integrity. It involves dividing large tables into smaller ones and defining relationships. Common forms include 1NF, 2NF, and 3NF.", "keywords": ["organizing", "redundancy", "integrity", "dividing", "relationships", "1NF", "2NF", "3NF"]},
            {"q": "Explain the difference between clustered and non-clustered indexes.", "ideal": "A clustered index determines the physical order of data in a table, so there can be only one per table. A non-clustered index stores a separate sorted logical structure that points to the data rows, and a table can have many.", "keywords": ["physical order", "only one", "separate", "sorted", "logical", "points", "many"]}
        ],
        "Case Study": [
            {"q": "How would you troubleshoot a slow database querying system?", "ideal": "I would use tools like EXPLAIN PLAN to analyze query execution paths. I'd look for missing indexes, full table scans, or outdated statistics. I would also check hardware constraints like CPU, memory, and disk I/O bottlenecks.", "keywords": ["EXPLAIN", "execution paths", "missing indexes", "table scans", "statistics", "hardware", "bottlenecks"]}
        ]
    },
    "Mobile App Developer": {
        "Technical": [
            {"q": "Explain the application lifecycle in iOS or Android.", "ideal": "In iOS, states include Not Running, Inactive, Active, Background, and Suspended. In Android, the lifecycle follows onCreate, onStart, onResume, onPause, onStop, and onDestroy callbacks. Proper handling ensures state preservation and battery efficiency.", "keywords": ["Inactive", "Active", "Background", "Suspended", "onCreate", "onResume", "onPause", "onDestroy", "preservation"]},
            {"q": "How do you manage memory limits in a mobile application?", "ideal": "I use lightweight data structures, load images asynchronously while caching them, and ensure there are no strong reference cycles (using weak references) to prevent memory leaks. Tools like Instruments or LeakCanary help profile memory usage.", "keywords": ["lightweight", "asynchronously", "caching", "reference cycles", "weak", "memory leaks", "LeakCanary"]}
        ],
         "Case Study": [
             {"q": "Design the architecture for an offline-first mobile app.", "ideal": "I'd use a local database (like SQLite, CoreData, or Room) as the single source of truth. Network requests would sync data in the background using work managers or background tasks, implementing conflict resolution strategies for when connectivity is restored.", "keywords": ["local database", "SQLite", "source of truth", "background", "work managers", "conflict resolution", "connectivity"]}
         ]
    },
    "QA Automation Engineer": {
        "Technical": [
            {"q": "What is the Page Object Model (POM) and why use it?", "ideal": "POM is a design pattern in test automation that creates an object repository for web UI elements. It enhances test maintenance and reduces code duplication because changes in the UI only require updates in the page class, not the tests.", "keywords": ["design pattern", "object repository", "maintenance", "duplication", "page class"]},
            {"q": "Explain the difference between Smoke, Sanity, and Regression testing.", "ideal": "Smoke testing verifies core functionality works basically. Sanity checks unscripted, logical flows on a new build. Regression testing comprehensively verifies that recent code changes haven't broken existing features.", "keywords": ["core functionality", "unscripted", "build", "comprehensively", "recent code", "broken"]}
        ],
        "System Design": [
             {"q": "How would you design a test automation framework from scratch?", "ideal": "I'd choose a tool like Selenium or Cypress, paired with a language like Python or JS. I'd implement the Page Object Model, integrate a reporting tool like Allure, set up parameterized data inputs, and link the suite to a CI/CD pipeline for nightly execution.", "keywords": ["Selenium", "Cypress", "Page Object Model", "reporting", "Allure", "parameterized", "CI/CD", "nightly"]}
        ]
    }
}

basic_questions = [
    {"q": "Tell me about yourself.", "ideal": "I have a background in technology and have been working on various projects over the years. I focus on delivering high-quality results and collaborating effectively with the team.", "keywords": ["background", "technology", "projects", "quality", "collaborating"]},
    {"q": "What are your greatest strengths?", "ideal": "My greatest strengths are my problem-solving skills, my ability to learn quickly, and my strong communication. I'm able to break down complex issues and find practical solutions.", "keywords": ["problem-solving", "learn quickly", "communication", "practical"]},
    {"q": "What is your greatest weakness?", "ideal": "I sometimes focus too much on small details, which can slow me down. However, I use project management software to keep track of the big picture and stay on schedule.", "keywords": ["details", "slow", "project management", "big picture", "schedule"]},
    {"q": "Where do you see yourself in five years?", "ideal": "In five years, I hope to be recognized as an expert in my field, taking on more leadership responsibilities and mentoring newer team members.", "keywords": ["expert", "leadership", "responsibilities", "mentoring"]},
    {"q": "Describe a difficult work situation and how you overcame it.", "ideal": "We had a tight deadline and a key team member was out. I reorganized the remaining tasks, communicated the risk to stakeholders, and we all put in extra effort to ship on time.", "keywords": ["deadline", "reorganized", "communicated", "stakeholders", "effort", "time"]},
    {"q": "Why do you want to work here?", "ideal": "I admire your company's innovative products and strong culture of continuous learning. I'm looking for an environment where I can grow and contribute significantly.", "keywords": ["innovative", "products", "culture", "learning", "grow", "contribute"]},
    {"q": "Why should we hire you?", "ideal": "I have the right mix of technical skills and team collaboration experience. I am driven to deliver quality software and have a proven track record of solving hard problems.", "keywords": ["technical skills", "collaboration", "quality", "track record", "solving"]},
    {"q": "What is your greatest professional achievement?", "ideal": "My greatest achievement was leading a cross-functional team to deliver a critical project two weeks ahead of schedule, which increased company revenue by 10%.", "keywords": ["leading", "cross-functional", "deliver", "ahead of schedule", "revenue"]},
    {"q": "Tell me about a time you failed.", "ideal": "I once underestimated the time required for a database migration. After missing the initial deadline, I communicated transparently with my manager, worked overtime to finish it, and learned to better pad my estimates.", "keywords": ["underestimated", "deadline", "communicated", "overtime", "learned", "estimates"]},
    {"q": "How do you handle stress and pressure?", "ideal": "I handle stress by breaking down large tasks into smaller, actionable steps. I also ensure I take brief breaks and maintain clear communication with my team about my workload.", "keywords": ["breaking down", "actionable steps", "breaks", "communication", "workload"]},
    {"q": "What are your salary expectations?", "ideal": "Based on my research and my level of experience, I am looking for a salary in the range of [X] to [Y]. However, I am flexible depending on the full benefits package and the nature of the role.", "keywords": ["research", "experience", "range", "flexible", "benefits"]},
    {"q": "What do you like to do outside of work?", "ideal": "Outside of work, I enjoy reading technology blogs, contributing to open source, and hiking to clear my mind and stay active.", "keywords": ["reading", "blogs", "open source", "hiking", "active"]},
    {"q": "How do you prioritize your work?", "ideal": "I prioritize my work by evaluating urgency and impact. I use tools like Jira and the Eisenhower Matrix to focus on what brings the most value to the business first.", "keywords": ["urgency", "impact", "tools", "Jira", "Eisenhower", "value"]},
    {"q": "What is your ideal work environment?", "ideal": "My ideal work environment is collaborative, transparent, and driven by results rather than micromanagement. I value open communication and opportunities for professional growth.", "keywords": ["collaborative", "transparent", "results", "open communication", "growth"]},
    {"q": "What coding language are you most comfortable with?", "ideal": "I am most comfortable with Python and JavaScript. I've used them extensively for backend services and frontend interfaces, but I adapt quickly to any syntax required by the project.", "keywords": ["Python", "JavaScript", "extensively", "adapt quickly", "syntax"]}
]

for role in existing_db:
    existing_db[role]["Basic"] = basic_questions

with open("questions.py", "w") as f:
    f.write("QUESTIONS_DB = " + json.dumps(existing_db, indent=4))
