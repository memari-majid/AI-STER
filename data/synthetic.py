"""
Synthetic data generation for testing AI-STER application
"""

import random
import uuid
from datetime import datetime, timedelta
from typing import List, Dict, Any
from .rubrics import get_field_evaluation_items, get_ster_items, get_professional_dispositions

# Sample names for synthetic data
STUDENT_NAMES = [
    "Emily Johnson", "Michael Chen", "Sarah Williams", "David Rodriguez", "Ashley Brown",
    "Christopher Lee", "Jessica Garcia", "Matthew Davis", "Amanda Wilson", "Daniel Martinez",
    "Samantha Anderson", "Joshua Thompson", "Lauren Miller", "Andrew Taylor", "Rachel Moore",
    "Kevin Jackson", "Nicole White", "Tyler Harris", "Megan Martin", "Brandon Clark",
    "Isabella Rodriguez", "Ethan Kim", "Olivia Thompson", "Noah Patel", "Sophia Wilson",
    "Jacob Martinez", "Emma Davis", "William Garcia", "Ava Anderson", "Mason Taylor"
]

EVALUATOR_NAMES = [
    "Dr. Sarah Mitchell", "Prof. James Rodriguez", "Ms. Maria Gonzalez", "Mr. Robert Thompson", "Dr. Lisa Williams",
    "Prof. Michael Davis", "Ms. Jennifer Miller", "Mr. David Wilson", "Dr. Karen Brown", "Prof. Steven Jones",
    "Ms. Ashley Garcia", "Mr. Daniel Martinez", "Dr. Rachel Taylor", "Prof. Christopher Moore", "Ms. Amanda Jackson",
    "Dr. Nicole Anderson", "Prof. Ryan Johnson", "Ms. Jessica Lee", "Mr. Kevin Smith", "Dr. Melissa White"
]

SUPERVISORS = [name for name in EVALUATOR_NAMES if name.startswith(("Dr.", "Prof."))]
COOPERATING_TEACHERS = [name for name in EVALUATOR_NAMES if name.startswith(("Ms.", "Mr."))]

# School settings for realistic contexts
SCHOOL_SETTINGS = [
    {"name": "Lincoln Elementary", "grade_levels": "K-5", "setting": "urban"},
    {"name": "Mountain View Middle School", "grade_levels": "6-8", "setting": "suburban"},
    {"name": "Sunset High School", "grade_levels": "9-12", "setting": "rural"},
    {"name": "Riverside Elementary", "grade_levels": "K-6", "setting": "suburban"},
    {"name": "Valley View High School", "grade_levels": "9-12", "setting": "urban"},
    {"name": "Pioneer Elementary", "grade_levels": "K-5", "setting": "rural"},
    {"name": "Oakwood Middle School", "grade_levels": "6-8", "setting": "suburban"},
    {"name": "Heritage High School", "grade_levels": "9-12", "setting": "suburban"},
    {"name": "Meadowbrook Elementary", "grade_levels": "K-5", "setting": "urban"},
    {"name": "Cedar Hills Middle School", "grade_levels": "6-9", "setting": "rural"}
]

# Subject areas for context
SUBJECT_AREAS = [
    "Mathematics", "English Language Arts", "Science", "Social Studies", "Art",
    "Music", "Physical Education", "Special Education", "ESL", "Technology"
]

# Student names for lesson plan rosters (different from student teacher names)
CLASSROOM_STUDENT_NAMES = [
    "Aiden Smith", "Bella Garcia", "Carter Johnson", "Destiny Rodriguez", "Ethan Williams",
    "Faith Martinez", "Gabriel Thompson", "Hannah Davis", "Isaac Brown", "Jasmine Wilson",
    "Kayden Anderson", "Luna Taylor", "Mason Clark", "Nora Lewis", "Oliver Walker",
    "Penelope Hall", "Quinn Allen", "Ruby Young", "Sebastian King", "Tiana Wright",
    "Uriah Lopez", "Violet Hill", "Wesley Green", "Ximena Adams", "Yusuf Baker",
    "Zoe Carter", "Adrian Mitchell", "Brooke Perez", "Caleb Roberts", "Delilah Turner",
    "Evan Phillips", "Fiona Campbell", "Grayson Parker", "Hazel Evans", "Ivan Edwards",
    "Jade Collins", "Kai Stewart", "Lily Sanchez", "Miles Morris", "Nova Rogers"
]

def generate_lesson_plan(student_name: str, subject_area: str, grade_levels: str, 
                        school_name: str, lesson_date: datetime) -> str:
    """Generate a realistic lesson plan with extractable information"""
    
    # Generate class size but don't include student names for privacy
    class_size = random.randint(18, 28)
    
    # Grade level specific topics
    topics_by_subject = {
        "Mathematics": {
            "K-5": ["Addition and Subtraction", "Multiplication Tables", "Fractions", "Geometry Shapes", "Place Value"],
            "6-8": ["Algebraic Expressions", "Ratios and Proportions", "Linear Equations", "Statistics", "Probability"],
            "9-12": ["Quadratic Functions", "Trigonometry", "Calculus Introduction", "Statistics and Data Analysis", "Polynomial Functions"]
        },
        "English Language Arts": {
            "K-5": ["Phonics and Reading", "Creative Writing", "Story Elements", "Grammar Basics", "Vocabulary Building"],
            "6-8": ["Literary Analysis", "Persuasive Writing", "Research Skills", "Poetry Study", "Narrative Writing"],
            "9-12": ["Shakespearean Literature", "Argumentative Essays", "Literary Criticism", "Creative Writing Workshop", "AP Literature"]
        },
        "Science": {
            "K-5": ["Plant Life Cycles", "Weather Patterns", "Simple Machines", "Animal Habitats", "States of Matter"],
            "6-8": ["Cell Structure", "Chemical Reactions", "Earth's Layers", "Energy and Motion", "Ecosystems"],
            "9-12": ["Genetics and DNA", "Chemical Bonding", "Physics of Motion", "Environmental Science", "Organic Chemistry"]
        },
        "Social Studies": {
            "K-5": ["Community Helpers", "American Symbols", "Map Skills", "Native American History", "Colonial America"],
            "6-8": ["Ancient Civilizations", "World Geography", "American Revolution", "Civil War", "Constitution Study"],
            "9-12": ["World War II", "Government Systems", "Economics Principles", "Modern World History", "Constitutional Law"]
        }
    }
    
    # Get appropriate topic based on subject and grade level
    grade_key = "K-5" if any(g in grade_levels for g in ["K", "1", "2", "3", "4", "5"]) else \
                "6-8" if any(g in grade_levels for g in ["6", "7", "8"]) else "9-12"
    
    topic = random.choice(topics_by_subject.get(subject_area, {}).get(grade_key, ["General Topic"]))
    
    # Select lesson plan format
    formats = ["detailed", "simple", "template", "narrative"]
    format_type = random.choice(formats)
    
    if format_type == "detailed":
        return f"""LESSON PLAN
        
Teacher: {student_name}
Date: {lesson_date.strftime('%B %d, %Y')}
School: {school_name}
Subject: {subject_area}
Grade Level: {grade_levels}
Class Period: {random.choice(['1st Period', '2nd Period', '3rd Period', '4th Period', 'Morning Block', 'Afternoon Block'])}
Duration: {random.choice(['50 minutes', '45 minutes', '90 minutes', '60 minutes'])}
Class Size: {class_size} students

LESSON TOPIC: {topic}

UTAH CORE STANDARDS:
{subject_area}.{random.randint(1,5)}.{random.randint(1,8)} - Students will demonstrate understanding of {topic.lower()}

LEARNING OBJECTIVES:
1. Students will be able to identify key concepts related to {topic.lower()}
2. Students will demonstrate comprehension through practical application
3. Students will collaborate effectively in small group activities

MATERIALS NEEDED:
- Whiteboard and markers
- Student worksheets
- {random.choice(['Textbooks', 'Tablets', 'Manipulatives', 'Art supplies', 'Science equipment'])}
- {random.choice(['Projector', 'Chart paper', 'Timer', 'Calculator', 'Reference materials'])}

LESSON STRUCTURE:

Opening (10 minutes):
- Welcome and attendance
- Review previous lesson on {random.choice(['related concepts', 'prerequisite skills', 'background knowledge'])}
- Introduce today's topic: {topic}

Direct Instruction (20 minutes):
- Present key concepts using visual aids
- Demonstrate problem-solving strategies
- Check for understanding through questioning

Guided Practice (15 minutes):
- Students work in pairs on practice problems
- Teacher circulates and provides support
- Address common misconceptions

Independent Practice (10 minutes):
- Individual worksheet completion
- Students apply learned concepts independently

Closure (5 minutes):
- Review key points from lesson
- Preview next lesson
- Assign homework if applicable

ASSESSMENT:
- Formative: Observation during guided practice
- Summative: Exit ticket with 3 key questions
- Accommodations: Extended time for students with IEPs

DIFFERENTIATION:
- Advanced learners: Extension activities
- Struggling learners: Simplified problems with visual supports
- ELL students: Vocabulary support and peer partnerships

HOMEWORK:
Practice worksheet pages {random.randint(1,50)}-{random.randint(51,100)}

REFLECTION NOTES:
[To be completed after lesson]
"""

    elif format_type == "simple":
        return f"""Lesson Plan - {lesson_date.strftime('%m/%d/%Y')}

Teacher: {student_name}
Subject: {subject_area} 
Topic: {topic}
Grade: {grade_levels}
School: {school_name}
Class Size: {class_size} students

Lesson Goals:
- Understand {topic.lower()}
- Practice key skills
- Complete assessment activity

Activities:
1. Warm-up review (10 min)
2. New material presentation (20 min)  
3. Practice exercises (15 min)
4. Wrap-up discussion (5 min)

Materials: textbook, worksheets, {random.choice(['calculator', 'manipulatives', 'art supplies'])}

Assessment: {random.choice(['Quiz', 'Worksheet', 'Oral questions', 'Group project'])}
"""

    elif format_type == "template":
        return f"""DAILY LESSON PLAN TEMPLATE

BASIC INFORMATION:
Teacher Name: {student_name}
Date: {lesson_date.strftime('%A, %B %d, %Y')}
Subject Area: {subject_area}
Grade Level(s): {grade_levels}
School: {school_name}
Class Size: {class_size} students

LESSON DETAILS:
Unit: {random.choice(['Unit 1', 'Unit 2', 'Unit 3', 'Chapter 5', 'Module 2'])}
Lesson Topic: {topic}
Time Allocation: {random.choice(['50 minutes', '45 minutes', '60 minutes'])}

STANDARDS ALIGNMENT:
Utah Core Standard: {subject_area}.{random.randint(1,6)}.{random.randint(1,10)}

LEARNING TARGETS:
□ I can explain {topic.lower()}
□ I can apply concepts to solve problems  
□ I can work collaboratively with peers

LESSON SEQUENCE:
Hook/Engagement (5 min): _______________
Direct Instruction (20 min): _______________
Guided Practice (15 min): _______________
Independent Work (10 min): _______________

MATERIALS & RESOURCES:
□ {random.choice(['Textbook', 'Workbook', 'Digital resources'])}
□ {random.choice(['Manipulatives', 'Art supplies', 'Science kit'])}
□ {random.choice(['Projector', 'Whiteboard', 'Chart paper'])}

POST-LESSON REFLECTION:
What worked well: _______________
What needs improvement: _______________
Next steps: _______________
"""

    else:  # narrative format
        return f"""Teaching Plan for {lesson_date.strftime('%B %d, %Y')}

Hello! I'm {student_name} and I'll be teaching {subject_area} today at {school_name}. 
My class has {class_size} wonderful students in grade {grade_levels}.

Today's lesson focuses on {topic}. I'm really excited to share this with my students!

We'll start with a fun warm-up activity to get everyone engaged. Then I'll introduce 
the main concepts through interactive demonstration. Students will work in small groups 
to practice what they've learned before completing individual exercises.

I've prepared {random.choice(['worksheets', 'digital activities', 'hands-on experiments'])} 
to help reinforce the learning objectives. The lesson should take about 
{random.choice(['45-50 minutes', '50-60 minutes', '90 minutes'])} to complete.

For assessment, I plan to use {random.choice(['exit tickets', 'peer evaluation', 'quick quiz', 'observation checklist'])} 
to check student understanding.

Materials needed:
- {random.choice(['Textbooks and notebooks', 'Tablets and digital resources', 'Art supplies and paper'])}
- {random.choice(['Calculator', 'Science equipment', 'Maps and globes', 'Musical instruments'])}
- {random.choice(['Projector screen', 'Whiteboard markers', 'Chart paper'])}

I'm looking forward to seeing how the students respond to this lesson on {topic}!

Reflection space (to be completed after teaching):
_______________________________________________
"""

def generate_synthetic_evaluations(
    count: int = 10,
    rubric_type: str = "both",
    score_distribution: str = "random"
) -> List[Dict[str, Any]]:
    """
    Generate synthetic evaluation data for testing
    
    Args:
        count: Number of evaluations to generate
        rubric_type: "field_evaluation", "ster", or "both"
        score_distribution: "random", "high_performing", "low_performing", "mixed"
    
    Returns:
        List of synthetic evaluation dictionaries
    """
    evaluations = []
    
    for i in range(count):
        # Determine rubric type for this evaluation
        if rubric_type == "both":
            eval_rubric_type = random.choice(["field_evaluation", "ster"])
        else:
            eval_rubric_type = rubric_type
        
        # Get appropriate items
        items = get_field_evaluation_items() if eval_rubric_type == "field_evaluation" else get_ster_items()
        dispositions = get_professional_dispositions()
        
        # Generate basic info
        student_name = random.choice(STUDENT_NAMES)
        evaluator_role = random.choice(["supervisor", "cooperating_teacher"])
        evaluator_name = random.choice(SUPERVISORS if evaluator_role == "supervisor" else COOPERATING_TEACHERS)
        
        # Add realistic school context
        school = random.choice(SCHOOL_SETTINGS)
        subject_area = random.choice(SUBJECT_AREAS)
        
        # Generate scores based on distribution
        scores = generate_scores(items, score_distribution)
        disposition_scores = generate_disposition_scores(dispositions, score_distribution)
        
        # Generate justifications based on actual rubric criteria
        justifications = generate_justifications(items, scores)
        
        # Calculate total score
        total_score = sum(scores.values())
        
        # Determine status - most evaluations should be completed
        # Only incomplete if there are failing scores that need remediation
        has_failing_scores = any(score < 2 for score in scores.values()) or any(score < 3 for score in disposition_scores.values())
        if has_failing_scores:
            status = random.choices(["draft", "completed"], weights=[0.6, 0.4])[0]
        else:
            status = random.choices(["draft", "completed"], weights=[0.15, 0.85])[0]
        
        # Generate realistic timestamps
        created_date = datetime.now() - timedelta(days=random.randint(0, 90))
        completed_date = None
        if status == "completed":
            # Completed evaluations typically take 1-7 days to finalize
            completed_date = created_date + timedelta(days=random.randint(1, 7), hours=random.randint(1, 12))
        
        # Determine semester context
        semester = random.choice(["Fall 2024", "Spring 2024", "Summer 2024", "Fall 2023"])
        
        # Generate lesson plan for this evaluation
        lesson_date = created_date - timedelta(days=random.randint(0, 7))  # Lesson a few days before evaluation
        lesson_plan = generate_lesson_plan(student_name, subject_area, school['grade_levels'], school['name'], lesson_date)
        
        evaluation = {
            'id': str(uuid.uuid4()),
            'student_name': student_name,
            'evaluator_name': evaluator_name,
            'evaluator_role': evaluator_role,
            'school_name': school['name'],
            'grade_levels': school['grade_levels'],
            'school_setting': school['setting'],
            'subject_area': subject_area,
            'semester': semester,
            'rubric_type': eval_rubric_type,
            'scores': scores,
            'justifications': justifications,
            'disposition_scores': disposition_scores,
            'total_score': total_score,
            'status': status,
            'created_at': created_date.isoformat(),
            'completed_at': completed_date.isoformat() if completed_date else None,
            'lesson_plan': lesson_plan,  # NEW: Add lesson plan to synthetic data
            'lesson_plan_analysis': None,  # Will be populated by AI extraction
            'is_synthetic': True,  # Flag to identify synthetic data
            'evaluation_context': f"{school['setting'].title()} school setting",
            'notes': f"Student teaching placement in {subject_area} at {school['name']}"
        }
        
        evaluations.append(evaluation)
    
    return evaluations

def generate_scores(items: List[Dict], distribution: str) -> Dict[str, int]:
    """Generate realistic scores for assessment items based on distribution pattern"""
    scores = {}
    
    for item in items:
        if distribution == "high_performing":
            # Mostly 2s and 3s (successful student teachers)
            score = random.choices([2, 3], weights=[0.7, 0.3])[0]
        elif distribution == "low_performing":
            # Struggling student teachers - mostly 1s and 2s, rare 0s
            score = random.choices([0, 1, 2], weights=[0.1, 0.6, 0.3])[0]
        elif distribution == "mixed":
            # Realistic distribution for typical student teachers
            score = random.choices([1, 2, 3], weights=[0.2, 0.6, 0.2])[0]
        else:  # random but realistic
            # Most student teachers score Level 2 (meeting expectations)
            score = random.choices([1, 2, 3], weights=[0.25, 0.55, 0.2])[0]
        
        scores[item['id']] = score
    
    return scores

def generate_disposition_scores(dispositions: List[Dict], distribution: str) -> Dict[str, int]:
    """Generate realistic disposition scores (1-4 scale, must be 3+ for completion)"""
    scores = {}
    
    for disposition in dispositions:
        if distribution == "high_performing":
            # Excellent student teachers - mostly 4s with some 3s
            score = random.choices([3, 4], weights=[0.3, 0.7])[0]
        elif distribution == "low_performing":
            # Struggling with dispositions - mix of 2s and 3s, rare 1s
            score = random.choices([1, 2, 3], weights=[0.1, 0.4, 0.5])[0]
        elif distribution == "mixed":
            # Typical student teachers - mostly 3s with some 4s, occasional 2s
            score = random.choices([2, 3, 4], weights=[0.15, 0.65, 0.2])[0]
        else:  # random but realistic
            # Most student teachers meet disposition requirements (3+)
            score = random.choices([3, 4], weights=[0.7, 0.3])[0]
        
        scores[disposition['id']] = score
    
    return scores

def generate_justifications(items: List[Dict], scores: Dict[str, int]) -> Dict[str, str]:
    """Generate realistic, rubric-based justifications for assessment items"""
    justifications = {}
    
    # Rubric-specific justification templates based on actual USBE criteria
    rubric_justifications = {
        'LL3': {
            0: "Student teacher was not observed addressing classroom norms or appeared unaware of existing behavioral expectations.",
            1: "Student teacher demonstrated understanding of the established classroom norms including behavioral and instructional procedures, but did not actively implement them.",
            2: "Student teacher effectively implemented classroom norms that promoted positive relationships, consistently reinforcing respectful interactions between teacher-student and student-student.",
            3: "Student teacher actively created and sustained classroom norms, taking initiative to foster positive relationships and modeling respectful behavior throughout all interactions."
        },
        'LL5': {
            0: "Student teacher did not communicate clear expectations and failed to use positive behavior interventions during the observation.",
            1: "Student teacher either communicated expectations or used some positive reinforcements, but not both consistently.",
            2: "Student teacher clearly communicated expectations and procedures while implementing positive behavior interventions to support student ownership of behavior.",
            3: "Student teacher not only communicated clear expectations and used positive interventions but also created meaningful opportunities for students to self-monitor their behavior."
        },
        'IC1_IC2': {
            0: "Lesson plans and instruction showed limited understanding of Utah Core Standards with misaligned learning intentions and success criteria.",
            1: "Student teacher showed some understanding of Utah Core Standards but created learning intentions that were inconsistently aligned to the standards.",
            2: "Student teacher demonstrated consistent understanding of Utah Core Standards and created learning intentions and success criteria that were clearly aligned to the standards.",
            3: "Student teacher meaningfully integrated content that aligned with Utah Core Standards, demonstrating deep understanding through innovative and purposeful connections."
        },
        'CC2': {
            0: "Classroom environment observations revealed instances where students were disrespectful to each other without intervention.",
            1: "Student teacher conveyed respect for students through their interactions and communication style.",
            2: "Student teacher created a classroom environment where students consistently demonstrated respect and value for each other during all observed activities.",
            3: "Student teacher explicitly taught students how to respect and value each other, providing direct instruction and modeling of these behaviors."
        },
        'CC3': {
            0: "No clear guidelines for behavior were established or communicated during the observation period.",
            1: "Student teacher established clear behavioral guidelines but did not involve students in their creation.",
            2: "Student teacher meaningfully involved students in establishing clear guidelines for behavior, ensuring student voice in the process.",
            3: "Student teacher engaged students in creating guidelines and fostered meaningful ownership of action steps and accountability for subsequent behavior."
        },
        'CC4': {
            0: "Physical and emotional safety concerns were observed but not addressed by the student teacher.",
            1: "Student teacher showed awareness of physical and emotional safety concerns but response was delayed or minimal.",
            2: "Student teacher promptly and appropriately addressed physical and emotional safety concerns as they arose during instruction.",
            3: "Student teacher proactively created an environment that prevented physical and emotional safety concerns through careful planning and awareness."
        },
        'CC6': {
            0: "Student teacher failed to implement effective classroom management strategies during the observed lesson.",
            1: "Student teacher used basic classroom management strategies but without strategic organization for optimal learning.",
            2: "Student teacher strategically organized the classroom environment and used effective instructional and management strategies that clearly promoted student learning.",
            3: "Student teacher expertly managed time, space, and attention to maximize student participation and create an optimal learning environment."
        },
        'CC8': {
            0: "Classroom environment appeared unsafe for student participation, with students hesitant to engage or participate.",
            1: "Most students participated in classroom activities, indicating a generally safe environment for engagement.",
            2: "Student teacher created an environment where students felt safe to participate and engage, with evidence of student comfort in sharing ideas.",
            3: "Student teacher encouraged an environment where students took academic risks as part of learning, supporting growth mindset and resilience."
        },
        'LL1': {
            0: "Student teacher worked in isolation and did not collaborate with or consider input from students' parents/guardians.",
            1: "Student teacher considered and incorporated input from students' parents/guardians in planning and instruction.",
            2: "Student teacher actively participated in a meeting with parents/guardians under mentor supervision, contributing meaningfully to discussions.",
            3: "Student teacher initiated communication with parents/guardians to design specific supports that met individual student needs."
        },
        'LL2': {
            0: "Instruction did not demonstrate awareness of learners' background knowledge or developmental needs.",
            1: "Student teacher demonstrated awareness of learners' background knowledge and needs by learning names and gathering contextual information.",
            2: "Student teacher designed learning experiences that clearly reflected understanding of learners' academic background knowledge and individual needs.",
            3: "Student teacher implemented and modified learning experiences based on specific learners' developmental levels, adjusting instruction throughout the lesson."
        },
        'LL4': {
            0: "No adaptations were made to instruction for learners of varied backgrounds during the observed lesson.",
            1: "Student teacher planned generic adaptations such as providing more time, but these may not have been appropriate for specific learners.",
            2: "Student teacher planned and implemented appropriate adaptations that were specifically designed for the diverse learners in the classroom.",
            3: "Student teacher planned appropriate adaptations and adjusted instruction based on developmental, cultural, or linguistic needs of individual students."
        },
        'LL6': {
            0: "Learning experiences and sources were not appropriate for the stated learning intentions and lacked relevance.",
            1: "Student teacher used appropriate content sources but lessons lacked real-world connections and relied heavily on textbook-centered instruction.",
            2: "Student teacher used appropriate sources and designed learning experiences with clear real-world connections using authentic media and community resources.",
            3: "Student teacher engaged learners in using multiple appropriate sources that fostered student ownership of authentic learning through meaningful real-world connections."
        },
        'LL7': {
            0: "No feedback was provided to students during the observed instruction period.",
            1: "Student teacher provided general feedback such as 'good job' but lacked specificity to guide student improvement.",
            2: "Student teacher provided specific and timely feedback and encouraged students to apply it to future performance and learning goals.",
            3: "Student teacher structured opportunities for students to apply feedback to improve their learning and engage in self-assessment of progress towards goals."
        },
        'IC1_IC2_STER': {
            0: "Lesson intentions and success criteria were missing or not aligned to Utah Core Standards, with limited understanding demonstrated.",
            1: "Student teacher showed inconsistent understanding of Utah Core Standards or created learning intentions with inconsistent alignment.",
            2: "Student teacher demonstrated consistent understanding of Utah Core Standards and created learning intentions and success criteria with clear alignment.",
            3: "Student teacher meaningfully integrated content aligned with Utah Core Standards, demonstrating sophisticated understanding and application."
        },
        'IC3': {
            0: "No evidence of learning objectives or intentions was apparent in the design of learning experiences.",
            1: "Student teacher inconsistently provided evidence of learning objectives or success criteria in lesson planning and delivery.",
            2: "Student teacher designed learning experiences that were clearly aligned to stated learning intentions and success criteria.",
            3: "Student teacher used students' responses to instruction to inform and adjust future lessons, demonstrating responsive teaching."
        },
        'A1': {
            0: "No assessment strategies were used to monitor student learning during the observed instruction.",
            1: "Student teacher used limited assessment strategies with minimal variety in monitoring student learning.",
            2: "Student teacher used multiple and varied assessment strategies to effectively monitor student learning throughout the lesson.",
            3: "Student teacher used assessment data to differentiate instruction for individual students, adjusting teaching based on student needs."
        },
        'A2': {
            0: "Assessment data was not analyzed or used to inform instructional decisions.",
            1: "Student teacher collected assessment data but did not analyze it to inform subsequent instruction.",
            2: "Student teacher analyzed assessment data and used it to make informed instructional decisions for future lessons.",
            3: "Student teacher used data analysis to modify instruction in real-time, adjusting teaching based on immediate student needs and responses."
        }
    }
    
    for item in items:
        score = scores.get(item['id'], 0)
        if score >= 2 or random.random() < 0.8:  # Generate more justifications for realistic evaluation
            item_id = item['id']
            if item_id in rubric_justifications:
                justifications[item_id] = rubric_justifications[item_id][score]
            else:
                # Fallback for any missing items
                generic_templates = {
                    0: f"The student teacher did not demonstrate competency in {item['title'].lower()}.",
                    1: f"The student teacher showed beginning development in {item['title'].lower()}.",
                    2: f"The student teacher effectively demonstrated {item['title'].lower()}.",
                    3: f"The student teacher exceeded expectations in {item['title'].lower()}."
                }
                justifications[item_id] = generic_templates[score]
    
    return justifications 