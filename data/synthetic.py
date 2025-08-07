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
    """Generate a realistic lesson plan aligned with Utah DOE standards and USBE evaluation criteria"""
    
    # Generate class size but don't include student names for privacy
    class_size = random.randint(18, 28)
    
    # Utah Core Standards-aligned topics with proper standard citations
    topics_by_subject = {
        "Mathematics": {
            "K-5": [
                {"topic": "Place Value and Number Sense", "standards": ["3.NBT.1", "3.NBT.2"], "description": "Use place value understanding to round whole numbers and fluently add and subtract within 1,000"},
                {"topic": "Multiplication and Division", "standards": ["3.OA.1", "3.OA.7"], "description": "Interpret products of whole numbers and fluently multiply and divide within 100"},
                {"topic": "Fractions", "standards": ["3.NF.1", "3.NF.2"], "description": "Understand fractions as numbers and represent fractions on number lines"},
                {"topic": "Measurement and Data", "standards": ["3.MD.3", "3.MD.8"], "description": "Draw scaled picture graphs and solve problems involving area and perimeter"}
            ],
            "6-8": [
                {"topic": "Ratios and Proportional Relationships", "standards": ["6.RP.1", "6.RP.3"], "description": "Understand concepts of ratios and use ratio reasoning to solve problems"},
                {"topic": "Expressions and Equations", "standards": ["7.EE.1", "7.EE.4"], "description": "Apply properties of operations to generate equivalent expressions"},
                {"topic": "Linear Functions", "standards": ["8.F.1", "8.F.3"], "description": "Understand functions and interpret functions that arise in applications"},
                {"topic": "Geometry and Measurement", "standards": ["7.G.1", "7.G.6"], "description": "Draw, construct, and describe geometrical figures and solve real-world problems"}
            ],
            "9-12": [
                {"topic": "Quadratic Functions", "standards": ["A.CED.1", "F.IF.7"], "description": "Create equations and graph functions to model relationships"},
                {"topic": "Statistics and Probability", "standards": ["S.ID.6", "S.CP.1"], "description": "Represent data and understand independence and conditional probability"},
                {"topic": "Trigonometry", "standards": ["G.SRT.6", "G.SRT.8"], "description": "Understand trigonometric ratios and solve problems involving right triangles"}
            ]
        },
        "English Language Arts": {
            "K-5": [
                {"topic": "Reading Comprehension and Theme", "standards": ["RL.3.2", "RL.3.1"], "description": "Determine central message and cite textual evidence to support analysis"},
                {"topic": "Narrative Writing", "standards": ["W.3.3", "W.3.4"], "description": "Write narratives to develop real or imagined experiences with clear sequence"},
                {"topic": "Language and Vocabulary", "standards": ["L.3.4", "L.3.5"], "description": "Determine meaning of unknown words and demonstrate understanding of word relationships"},
                {"topic": "Speaking and Listening", "standards": ["SL.3.1", "SL.3.4"], "description": "Engage in collaborative discussions and report on topics with appropriate facts"}
            ],
            "6-8": [
                {"topic": "Literary Analysis and Theme", "standards": ["RL.6.2", "RL.6.1"], "description": "Determine theme and cite textual evidence to support analysis"},
                {"topic": "Argumentative Writing", "standards": ["W.7.1", "W.7.4"], "description": "Write arguments to support claims with clear reasons and relevant evidence"},
                {"topic": "Research and Inquiry", "standards": ["W.7.7", "W.7.8"], "description": "Conduct research projects and gather relevant information from multiple sources"},
                {"topic": "Language Conventions", "standards": ["L.7.1", "L.7.2"], "description": "Demonstrate command of conventions and use knowledge of language"}
            ],
            "9-12": [
                {"topic": "Literary Criticism and Analysis", "standards": ["RL.11-12.4", "RL.11-12.6"], "description": "Analyze author's choices and determine point of view in complex texts"},
                {"topic": "Research and Argumentation", "standards": ["W.11-12.1", "W.11-12.7"], "description": "Write arguments and conduct sustained research projects"},
                {"topic": "Language and Style", "standards": ["L.11-12.3", "L.11-12.5"], "description": "Apply knowledge of language and demonstrate understanding of figurative language"}
            ]
        },
        "Science": {
            "K-5": [
                {"topic": "Forces and Motion", "standards": ["5.PS.2.1", "K.PS.2.1"], "description": "Support arguments about gravitational force and analyze data from pushes and pulls"},
                {"topic": "Life Science Systems", "standards": ["4.LS.1.1", "3.LS.3.1"], "description": "Construct arguments about plant/animal structures and analyze life cycles"},
                {"topic": "Earth and Space", "standards": ["5.ESS.1.2", "K.ESS.2.1"], "description": "Represent data to reveal patterns in daily changes and weather patterns"}
            ],
            "6-8": [
                {"topic": "Cell Structure and Function", "standards": ["MS.LS.1.1", "MS.LS.1.2"], "description": "Conduct investigations about cells and develop models of cell parts"},
                {"topic": "Energy and Matter", "standards": ["MS.PS.3.3", "MS.PS.1.2"], "description": "Apply scientific principles and analyze data on properties of substances"},
                {"topic": "Earth Systems", "standards": ["MS.ESS.2.1", "MS.ESS.3.3"], "description": "Develop models of Earth's systems and analyze human impact on environment"}
            ],
            "9-12": [
                {"topic": "Genetics and Evolution", "standards": ["HS.LS.3.2", "HS.LS.4.1"], "description": "Make claims about inheritance and communicate about common ancestry"},
                {"topic": "Chemical Reactions", "standards": ["HS.PS.1.2", "HS.PS.1.7"], "description": "Construct explanations and use mathematical representations for reactions"},
                {"topic": "Earth and Climate", "standards": ["HS.ESS.3.5", "HS.ESS.2.2"], "description": "Analyze climate models and analyze geoscience data"}
            ]
        },
        "Social Studies": {
            "K-5": [
                {"topic": "Community and Citizenship", "standards": ["2.C.1", "3.C.2"], "description": "Explain how people make rules and describe civic ideals and practices"},
                {"topic": "Geography and Culture", "standards": ["3.G.2", "2.G.1"], "description": "Use geographic tools and explain how culture influences communities"},
                {"topic": "Historical Thinking", "standards": ["4.H.2", "1.H.1"], "description": "Analyze chronology of events and create historical narratives"}
            ],
            "6-8": [
                {"topic": "Ancient Civilizations", "standards": ["6.H.1", "6.G.1"], "description": "Analyze how geography influenced civilizations and compare ancient societies"},
                {"topic": "Constitutional Principles", "standards": ["8.C.1", "8.C.2"], "description": "Analyze how Constitution protects rights and evaluate democratic institutions"},
                {"topic": "Economic Systems", "standards": ["7.E.1", "6.E.1"], "description": "Analyze economic decisions and explain how trade connects societies"}
            ],
            "9-12": [
                {"topic": "Global Conflicts and Cooperation", "standards": ["HS.H.3", "HS.G.2"], "description": "Evaluate historical events and analyze spatial patterns of human-environment interactions"},
                {"topic": "Political Systems", "standards": ["HS.C.2", "HS.C.3"], "description": "Evaluate effectiveness of institutions and analyze impact of constitutions"},
                {"topic": "Economic Policy", "standards": ["HS.E.2", "HS.E.1"], "description": "Analyze economic policies and generate explanations for economic outcomes"}
            ]
        }
    }
    
    # Get appropriate topic based on subject and grade level
    grade_key = "K-5" if any(g in grade_levels for g in ["K", "1", "2", "3", "4", "5"]) else \
                "6-8" if any(g in grade_levels for g in ["6", "7", "8"]) else "9-12"
    
    topic_info = random.choice(topics_by_subject.get(subject_area, {}).get(grade_key, [{"topic": "General Topic", "standards": ["N/A"], "description": "General learning objective"}]))
    
    # Generate USBE-aligned lesson plan following the provided example format
    return f"""Lesson Plan: {topic_info['topic']}

Grade Level: {grade_levels}
Content Area: {subject_area}
Duration: {random.choice(['45 minutes', '50 minutes', '60 minutes', '90 minutes'])}
Teacher: {student_name}
School: {school_name}
Date: {lesson_date.strftime('%B %d, %Y')}
Class Size: {class_size} students

Utah {subject_area} Core Standards Addressed:
{chr(10).join([f"- {standard}: {topic_info['description']}" for standard in topic_info['standards']])}

Learning Intentions (IC2):
Students will be able to {topic_info['description'].lower()}.

Success Criteria (IC2):
- I can {random.choice(['identify and explain', 'analyze and interpret', 'create and demonstrate', 'compare and evaluate'])} {random.choice(['key concepts', 'main ideas', 'important relationships', 'essential elements'])} related to {topic_info['topic'].lower()}.
- I can {random.choice(['use appropriate vocabulary', 'apply learned concepts', 'make connections', 'provide evidence'])} to {random.choice(['support my understanding', 'explain my thinking', 'demonstrate learning', 'solve problems'])}.

Lesson Sequence:

1. Anticipatory Set ({random.choice(['5', '8', '10'])} minutes)
- {random.choice(['Display an engaging question or image', 'Share a real-world connection', 'Review prior learning', 'Present an intriguing scenario'])} related to {topic_info['topic']}.
- {random.choice(['Quick-write', 'Think-pair-share', 'Gallery walk', 'Class discussion'])}: Students activate prior knowledge.
- Connect to previous learning and preview today's objectives (LL2, IC4).

2. Direct Instruction ({random.choice(['10', '15', '20'])} minutes)
- {random.choice(['Review key concepts using visual aids', 'Model problem-solving strategies', 'Demonstrate procedures step-by-step', 'Present information using multimedia'])} (IC1).
- Use {random.choice(['anchor charts', 'graphic organizers', 'interactive demonstrations', 'digital presentations'])} to support understanding.
- Check for understanding through {random.choice(['questioning', 'thumbs up/down', 'exit tickets', 'partner discussions'])} (LL7).

3. Guided Practice ({random.choice(['15', '20', '25'])} minutes)
- {random.choice(['Students work in pairs', 'Small group investigation', 'Collaborative problem-solving', 'Structured practice activities'])} (CC2, CC3).
- Teacher {random.choice(['circulates and provides feedback', 'facilitates discussions', 'addresses misconceptions', 'differentiates support'])} (LL2, LL4).
- Students {random.choice(['complete practice problems', 'analyze examples', 'create models', 'discuss findings'])} with scaffolded support.

4. Independent Practice ({random.choice(['10', '15', '20'])} minutes)
- Students {random.choice(['complete individual tasks', 'apply concepts independently', 'create original work', 'solve challenge problems'])} to demonstrate understanding.
- {random.choice(['Worksheet completion', 'Digital activity', 'Creative project', 'Problem-solving task'])} aligned to learning objectives.

5. Closure ({random.choice(['5', '8', '10'])} minutes)
- Students {random.choice(['summarize key learnings', 'share insights with class', 'complete exit ticket', 'reflect on progress'])} (LL7).
- Preview connections to future learning and homework expectations.

Differentiation Strategies (LL4, IP1):
- {random.choice(['Provide sentence frames for struggling writers', 'Offer visual supports and manipulatives', 'Use tiered assignments', 'Provide choice in demonstration methods'])}.
- {random.choice(['Extended time for processing', 'Alternative assessment formats', 'Peer partnerships', 'Technology assistance'])} for students with IEPs/504 plans.
- {random.choice(['Enrichment activities for advanced learners', 'Challenge problems', 'Independent research opportunities', 'Peer tutoring roles'])}.

Formative Assessment (A1, A2):
- {random.choice(['Exit tickets', 'Observation checklists', 'Quick polls', 'Self-assessment rubrics'])}
- {random.choice(['Informal checks during group work', 'Digital response systems', 'Student conferences', 'Portfolio artifacts'])}
- {random.choice(['Peer feedback sessions', 'Learning logs', 'Gallery walks', 'Thumbs up/down checks'])}

Real-World Connections (LL6):
- {random.choice(['Connect to students everyday experiences', 'Explore community applications', 'Discuss current events', 'Examine career connections'])} related to {topic_info['topic']}.
- Students explore how {random.choice(['these concepts apply to their lives', 'this learning connects to their interests', 'they can use this knowledge', 'this relates to their goals'])}.

Classroom Climate (CC2, CC3, CC8):
- Students work in {random.choice(['collaborative pairs', 'diverse groups', 'flexible partnerships'])} with {random.choice(['rotating roles', 'clear expectations', 'established norms'])}.
- {random.choice(['Review and reinforce', 'Establish and practice', 'Model and demonstrate'])} norms for {random.choice(['respectful listening', 'academic discussion', 'collaborative work', 'inclusive participation'])}.
- Create safe environment for {random.choice(['risk-taking', 'question-asking', 'idea-sharing', 'mistake-making'])} and learning.

Technology Integration (IP8):
- Use {random.choice(['Google Slides for presentations', 'Digital tools for creation', 'Online simulations', 'Interactive whiteboard'])} to enhance learning.
- {random.choice(['Student devices for research', 'Collaborative documents', 'Educational apps', 'Virtual manipulatives'])} support lesson objectives.
- {random.choice(['Digital portfolios', 'Online discussions', 'Multimedia projects', 'Assessment platforms'])} for student engagement.

Materials and Resources:
- {random.choice(['Utah Core Standards-aligned textbooks', 'Digital resources and websites', 'Hands-on manipulatives', 'Primary source documents'])}
- {random.choice(['Graphic organizers', 'Assessment rubrics', 'Reference materials', 'Interactive tools'])}
- {random.choice(['Projector and screen', 'Student tablets/laptops', 'Chart paper and markers', 'Laboratory equipment'])}

Homework/Extension (LL6):
- {random.choice(['Practice problems aligned to objectives', 'Reading assignment with reflection', 'Family interview or survey', 'Real-world application task'])}
- Students {random.choice(['prepare for next lesson', 'extend their learning', 'make home connections', 'practice key skills'])}

Professional Learning Connections:
This lesson aligns with Utah Core Standards and USBE evaluation criteria, supporting student achievement and demonstrating effective teaching practices across multiple rubric areas including IC1, IC2, LL2, LL4, LL6, LL7, CC2, CC3, CC8, A1, A2, and IP1, IP8.

Reflection Notes:
[To be completed after lesson implementation]
- What evidence shows students met learning objectives?
- How effectively did differentiation strategies support all learners?
- What adjustments would improve future instruction?
- How did classroom climate support learning?"""

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
        evaluator_role = "supervisor"  # Only supervisors in the system now
        evaluator_name = random.choice(SUPERVISORS)
        
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
        
        # Generate lesson plan for this evaluation (using Utah DOE-aligned format)
        lesson_date = created_date - timedelta(days=random.randint(0, 7))  # Lesson a few days before evaluation
        from .utah_lesson_plans import generate_utah_aligned_lesson_plan
        lesson_plan = generate_utah_aligned_lesson_plan(student_name, subject_area, school['grade_levels'], school['name'], lesson_date)
        
        # Map grade levels to departments
        grade_level = school['grade_levels']
        if 'K-' in grade_level or 'K-5' in grade_level or '1-' in grade_level or '2-' in grade_level or '3-' in grade_level:
            department = "Elementary"
        elif '6-' in grade_level or '7-' in grade_level or '8-' in grade_level or '9-' in grade_level or 'High' in grade_level:
            department = "Secondary"
        elif 'Special' in subject_area or 'SPED' in subject_area:
            department = "Special Ed"
        else:
            department = random.choice(["Elementary", "Secondary", "GRAD", "Special Ed"])
        
        evaluation = {
            'id': str(uuid.uuid4()),
            'student_name': student_name,
            'evaluator_name': evaluator_name,
            'evaluator_role': evaluator_role,
            'school_name': school['name'],
            'grade_levels': school['grade_levels'],
            'school_setting': school['setting'],
            'subject_area': subject_area,
            'department': department,  # NEW: Add department field
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