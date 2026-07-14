LANGUAGE_DB = {
    "Python": [
        {"q": "What is a list comprehension in Python?", "ideal": "It's a really short, clean way to make a new list out of an old one using just one line of code.", "keywords": ["short", "clean", "new list", "one line"]},
        {"q": "How is a tuple different from a list?", "ideal": "A tuple cannot be changed after you make it, but a list can be modified anytime.", "keywords": ["cannot be changed", "modified anytime"]},
        {"q": "What does 'yield' do in Python?", "ideal": "It turns a normal function into a generator. It sends a value back but saves its spot to pick up right where it left off next time.", "keywords": ["generator", "sends value", "saves spot", "left off"]},
    ],
    "JavaScript": [
        {"q": "What is the difference between let and var?", "ideal": "'let' is safer because it keeps a variable trapped inside the specific block of code where you made it. 'var' behaves weirdly and can leak out of blocks.", "keywords": ["safer", "trapped", "block", "var", "leak"]},
        {"q": "What is a Promise in JavaScript?", "ideal": "It's an object that beautifully handles work that takes time, like asking for data over the internet. It guarantees it will 'resolve' with data or 'reject' with an error eventually.", "keywords": ["handles work", "takes time", "internet", "resolve", "reject"]},
        {"q": "Explain 'this' in JavaScript.", "ideal": "'this' normally refers to the specific object that is currently running the code. Its value totally depends on exactly how a function was called.", "keywords": ["specific object", "running", "depends", "how function called"]},
    ],
    "Java": [
        {"q": "What is the difference between equals() and == in Java?", "ideal": "'==' checks if two things perfectly point to the exact same spot in memory. 'equals()' actually checks if the text or data inside them matches.", "keywords": ["point", "same spot", "memory", "text", "inside", "matches"]},
        {"q": "What is a NullPointerException?", "ideal": "It totally happens when you try to use a piece of code or variable that has absolutely nothing (null) stored inside it yet.", "keywords": ["use", "variable", "nothing", "null", "stored"]},
        {"q": "Why is the 'final' keyword used?", "ideal": "It smartly locks things down. If you put it on a variable, the value can never sadly change. On a class, it strictly means no other class can inherit from it.", "keywords": ["locks", "variable", "never change", "class", "inherit"]},
    ],
    "C++": [
        {"q": "What is a pointer?", "ideal": "It's a special variable that strictly holds the memory address of another variable, instead of holding normal data.", "keywords": ["special variable", "memory address", "holding data"]},
        {"q": "What is the difference between new and malloc()?", "ideal": "'new' creates an object and neatly calls its constructor to set it up perfectly. 'malloc' just grabs raw empty memory without setting anything up.", "keywords": ["creates object", "constructor", "set it up", "grabs memory", "empty"]},
        {"q": "Explain what a smart pointer is.", "ideal": "It's a wrapper that totally cleans up after itself. When you stop using a smart pointer, it strictly deletes the memory automatically so you don't get memory leaks.", "keywords": ["wrapper", "cleans up", "deletes memory", "automatically", "memory leaks"]},
    ],
    "SQL": [
        {"q": "What is the difference between INNER JOIN and LEFT JOIN?", "ideal": "INNER JOIN only gives you rows that perfectly match in both tables. LEFT JOIN gives you literally everything from the first table, plus matching rows from the second.", "keywords": ["gives rows", "match both", "everything", "first table", "plus matching"]},
        {"q": "What does a GROUP BY do?", "ideal": "It nicely squishes rows that share the totally same values into helpful summary rows, often used to neatly count, add, or average things.", "keywords": ["squishes", "same values", "summary rows", "count", "add", "average"]},
        {"q": "What's a primary key?", "ideal": "It is a totally unique ID number for every single row in a table. It strictly promises that no two rows can wildly share the same exact key.", "keywords": ["unique ID", "every row", "promises", "no two rows", "same key"]},
    ]
}
