"""
Utah Department of Education Aligned Lesson Plan Generation
Based on research of Utah State Board of Education approved formats and standards
"""

import random
from datetime import datetime
from typing import Dict, List, Any

def generate_utah_aligned_lesson_plan(student_name: str, subject_area: str, grade_levels: str, 
                                     school_name: str, lesson_date: datetime) -> str:
    """Generate a realistic lesson plan aligned with Utah DOE standards and approved formats"""
    
    # Generate class size but don't include student names for privacy
    class_size = random.randint(18, 28)
    
    # Utah Core Standards-aligned topics with proper standard citations
    topics_by_subject = {
        "Mathematics": {
            "K-5": [
                {"topic": "Place Value and Base Ten", "standard": "1.NBT.4", "description": "Add within 100 using place value understanding"},
                {"topic": "Place Value Understanding", "standard": "3.NBT.1", "description": "Use place value understanding to round whole numbers"},
                {"topic": "Addition and Subtraction Strategies", "standard": "3.NBT.2", "description": "Fluently add and subtract within 1,000 using strategies and algorithms"},
                {"topic": "Multiplication Concepts", "standard": "3.OA.1", "description": "Interpret products of whole numbers"},
                {"topic": "Two-Step Word Problems", "standard": "3.OA.8", "description": "Solve two-step word problems using four operations"},
                {"topic": "Fractions on Number Lines", "standard": "3.NF.2", "description": "Understand fractions as numbers on the number line"},
                {"topic": "Measurement and Data", "standard": "3.MD.3", "description": "Draw scaled picture graphs and solve problems using the information"},
                {"topic": "Area and Perimeter", "standard": "3.MD.8", "description": "Solve real world problems involving perimeters and areas"},
                {"topic": "Volume and Measurement", "standard": "5.MD.4", "description": "Measure volumes by counting unit cubes"},
                {"topic": "Volume Word Problems", "standard": "5.MD.5", "description": "Relate volume to multiplication and addition"}
            ],
            "6-8": [
                {"topic": "Ratios and Proportional Relationships", "standard": "6.RP.1", "description": "Understand concepts of ratios and rates"},
                {"topic": "Linear Equations", "standard": "8.EE.6", "description": "Use similar triangles to explain slope"},
                {"topic": "Algebraic Expressions", "standard": "7.EE.4", "description": "Use variables to represent quantities"},
                {"topic": "Statistics and Probability", "standard": "7.SP.6", "description": "Approximate probability of chance events"},
                {"topic": "Geometric Constructions", "standard": "7.G.2", "description": "Draw geometric shapes with given conditions"}
            ],
            "9-12": [
                {"topic": "Quadratic Functions", "standard": "A.CED.1", "description": "Create equations and inequalities in one variable"},
                {"topic": "Exponential Functions", "standard": "F.LE.2", "description": "Construct linear and exponential functions"},
                {"topic": "Trigonometric Ratios", "standard": "G.SRT.6", "description": "Understand sine, cosine, and tangent ratios"},
                {"topic": "Statistical Analysis", "standard": "S.ID.6", "description": "Represent data on two quantitative variables"},
                {"topic": "Polynomial Operations", "standard": "A.APR.1", "description": "Add, subtract, and multiply polynomials"}
            ]
        },
        "English Language Arts": {
            "K-5": [
                {"topic": "Personal Narrative Writing", "standard": "1.W.3", "description": "Write narratives in which they recount events and provide reactions"},
                {"topic": "Informative Writing", "standard": "2.W.2", "description": "Write informative/explanatory texts to examine a topic"},
                {"topic": "Reading Comprehension Strategies", "standard": "3.RL.2", "description": "Recount stories and determine central message or lesson"},
                {"topic": "Narrative Writing", "standard": "3.W.3", "description": "Write narratives to develop real or imagined experiences"},
                {"topic": "Informative Writing Advanced", "standard": "5.W.2", "description": "Write informative/explanatory texts to examine a topic and convey ideas clearly"},
                {"topic": "Vocabulary Acquisition", "standard": "3.L.4", "description": "Determine meaning of unknown words and phrases"},
                {"topic": "Text Features and Organization", "standard": "3.RI.5", "description": "Use text features to locate information efficiently"},
                {"topic": "Speaking and Listening Skills", "standard": "3.SL.1", "description": "Engage effectively in collaborative discussions"}
            ],
            "6-8": [
                {"topic": "Literary Analysis", "standard": "7.RL.2", "description": "Determine theme and analyze its development"},
                {"topic": "Argumentative Writing", "standard": "7.W.1", "description": "Write arguments to support claims with clear reasons"},
                {"topic": "Research and Inquiry", "standard": "7.W.7", "description": "Conduct short research projects"},
                {"topic": "Language Conventions", "standard": "7.L.1", "description": "Demonstrate command of conventions of standard English"},
                {"topic": "Media Literacy", "standard": "7.SL.2", "description": "Analyze main ideas and supporting details from diverse media"}
            ],
            "9-12": [
                {"topic": "Literary Criticism", "standard": "11-12.RL.4", "description": "Determine meaning of words and phrases including figurative meanings"},
                {"topic": "Rhetorical Analysis", "standard": "11-12.RI.6", "description": "Determine author's point of view and analyze rhetoric"},
                {"topic": "Research Writing", "standard": "11-12.W.7", "description": "Conduct sustained research projects"},
                {"topic": "Collaborative Discussion", "standard": "11-12.SL.1", "description": "Initiate and participate effectively in discussions"},
                {"topic": "Language Usage", "standard": "11-12.L.3", "description": "Apply knowledge of language to make effective choices"}
            ]
        },
        "Science": {
            "K-5": [
                {"topic": "Plant and Animal Structures", "standard": "4.LS.1.1", "description": "Construct an argument for how plant and animal structures function"},
                {"topic": "Weather Patterns", "standard": "K.ESS.2.1", "description": "Use observations to describe patterns of weather"},
                {"topic": "Forces and Motion", "standard": "5.PS.2.1", "description": "Support an argument about gravitational force"},
                {"topic": "Matter Properties", "standard": "2.PS.1.1", "description": "Plan and conduct investigation to describe and classify materials"},
                {"topic": "Earth's Surface Changes", "standard": "2.ESS.1.1", "description": "Use information from sources to describe Earth's features"}
            ],
            "6-8": [
                {"topic": "Cell Structure and Function", "standard": "MS.LS.1.1", "description": "Conduct investigation to provide evidence that living things are made of cells"},
                {"topic": "Chemical Reactions", "standard": "MS.PS.1.2", "description": "Analyze and interpret data on properties of substances"},
                {"topic": "Earth's Systems", "standard": "MS.ESS.2.1", "description": "Develop model to describe cycling of Earth's materials"},
                {"topic": "Energy Transfer", "standard": "MS.PS.3.3", "description": "Apply scientific principles to design heating or cooling device"},
                {"topic": "Ecosystem Interactions", "standard": "MS.LS.2.1", "description": "Analyze data to provide evidence for effects of resource availability"}
            ],
            "9-12": [
                {"topic": "Genetic Inheritance", "standard": "HS.LS.3.2", "description": "Make and defend claim based on evidence about inheritance"},
                {"topic": "Chemical Bonding", "standard": "HS.PS.1.2", "description": "Construct explanations for properties of substances"},
                {"topic": "Energy and Matter", "standard": "HS.PS.3.1", "description": "Create computational model to calculate change in energy"},
                {"topic": "Evolution Evidence", "standard": "HS.LS.4.1", "description": "Communicate scientific information about common ancestry"},
                {"topic": "Climate Systems", "standard": "HS.ESS.3.5", "description": "Analyze results from global climate models"}
            ]
        },
        "Social Studies": {
            "K-5": [
                {"topic": "Community and Government", "standard": "2.C.1", "description": "Explain how groups of people make rules to create responsibilities"},
                {"topic": "Geography and Maps", "standard": "3.G.2", "description": "Use maps, photos, and geographic tools to locate and describe places"},
                {"topic": "Historical Thinking", "standard": "4.H.2", "description": "Analyze the chronology of key historical events in Utah"},
                {"topic": "Economic Principles", "standard": "1.E.1", "description": "Explain how scarcity requires people to make choices"},
                {"topic": "Cultural Diversity", "standard": "2.C.4", "description": "Explain how people from various cultures live and work together"}
            ],
            "6-8": [
                {"topic": "Ancient Civilizations", "standard": "6.H.1", "description": "Analyze how physical geography influenced ancient civilizations"},
                {"topic": "Constitutional Principles", "standard": "8.C.1", "description": "Analyze how the Constitution protects rights"},
                {"topic": "Economic Systems", "standard": "7.E.1", "description": "Analyze how economic decisions affect individuals and groups"},
                {"topic": "Geographic Reasoning", "standard": "6.G.3", "description": "Explain how cultural and environmental characteristics vary"},
                {"topic": "Historical Context", "standard": "8.H.2", "description": "Evaluate the significance of major events in forming U.S. identity"}
            ],
            "9-12": [
                {"topic": "Global Conflicts", "standard": "HS.H.3", "description": "Evaluate how major historical events are interpreted"},
                {"topic": "Economic Policy", "standard": "HS.E.2", "description": "Analyze how economic policies affect domestic and global markets"},
                {"topic": "Political Systems", "standard": "HS.C.2", "description": "Evaluate citizens' and institutions' effectiveness"},
                {"topic": "Geographic Analysis", "standard": "HS.G.1", "description": "Use geospatial technologies to analyze geographic problems"},
                {"topic": "Historical Methodology", "standard": "HS.H.1", "description": "Analyze how historical context influences perspectives"}
            ]
        }
    }
    
    # Get appropriate topic based on subject and grade level
    grade_key = "K-5" if any(g in grade_levels for g in ["K", "1", "2", "3", "4", "5"]) else \
                "6-8" if any(g in grade_levels for g in ["6", "7", "8"]) else "9-12"
    
    topic_info = random.choice(topics_by_subject.get(subject_area, {}).get(grade_key, [{"topic": "General Topic", "standard": "N/A", "description": "General learning objective"}]))
    
    # Select lesson plan format based on Utah DOE approved formats
    formats = ["utah_detailed", "utah_core_guide", "uen_format", "usbe_template"]
    format_type = random.choice(formats)
    
    if format_type == "utah_detailed":
        return f"""UTAH LESSON PLAN

BASIC INFORMATION:
Teacher: {student_name}
Date: {lesson_date.strftime('%A, %B %d, %Y')}
School: {school_name}
Subject: {subject_area}
Grade Level(s): {grade_levels}
Class Size: {class_size} students
Duration: {random.choice(['50 minutes', '45 minutes', '90 minutes', '60 minutes'])}

STANDARDS ALIGNMENT:
Utah Core Standard: {topic_info['standard']}
Standard Description: {topic_info['description']}

LESSON TOPIC: {topic_info['topic']}

LESSON PERFORMANCE EXPECTATIONS:
- Students will {topic_info['description'].lower()}
- Students will demonstrate understanding through {random.choice(['practical application', 'collaborative discussion', 'written assessment', 'hands-on activities'])}
- Students will connect learning to {random.choice(['real-world applications', 'prior knowledge', 'future learning', 'cross-curricular concepts'])}

STUDENT BACKGROUND KNOWLEDGE:
- {random.choice(['Understanding of basic concepts from previous unit', 'Familiarity with academic vocabulary', 'Prior experience with similar problems', 'Foundation skills from earlier grades'])}
- {random.choice(['Ability to work collaboratively', 'Basic technology skills', 'Reading comprehension at grade level', 'Mathematical reasoning skills'])}

ACADEMIC VOCABULARY:
{random.choice(['analyze, synthesize, evaluate', 'compare, contrast, categorize', 'predict, hypothesize, conclude', 'sequence, organize, classify'])}

MATERIALS AND RESOURCES:
- {random.choice(['Interactive whiteboard', 'Document camera', 'Tablets/Chromebooks', 'Manipulatives'])}
- {random.choice(['Utah Core Standards materials', 'Grade-level textbooks', 'Digital resources', 'Hands-on materials'])}
- {random.choice(['Assessment rubrics', 'Graphic organizers', 'Reference materials', 'Calculator/tools'])}

LESSON STRUCTURE (5E Model):

Engage (10 minutes):
- {random.choice(['Hook activity related to student interests', 'Review previous learning connections', 'Present real-world problem scenario', 'Activate prior knowledge through discussion'])}
- Introduce learning targets and success criteria
- Preview lesson activities and expectations

Explore (20 minutes):
- {random.choice(['Guided discovery activity', 'Collaborative investigation', 'Hands-on exploration', 'Digital simulation or tool use'])}
- Students work in {random.choice(['pairs', 'small groups', 'collaborative teams'])} to explore key concepts
- Teacher facilitates and provides support as needed

Explain (15 minutes):
- Students share findings and observations
- Teacher connects student discoveries to formal concepts
- Introduce academic vocabulary in context
- Address misconceptions and clarify understanding

Elaborate (10 minutes):
- {random.choice(['Apply concepts to new situations', 'Extend learning through challenging problems', 'Connect to real-world applications', 'Cross-curricular connections'])}
- Students demonstrate understanding through application

Evaluate (5 minutes):
- {random.choice(['Exit ticket assessment', 'Quick formative check', 'Peer evaluation activity', 'Self-reflection prompt'])}
- Preview next lesson connections

ASSESSMENT STRATEGIES:
Formative Assessment:
- {random.choice(['Observation during group work', 'Check for understanding questions', 'Individual whiteboards', 'Digital response tools'])}
- {random.choice(['Peer discussion monitoring', 'Quick polls or thumbs up/down', 'Work samples review', 'Verbal questioning'])}

Summative Assessment:
- {random.choice(['Unit test questions', 'Performance task', 'Portfolio artifacts', 'Project components'])}

DIFFERENTIATION STRATEGIES:
Advanced Learners:
- {random.choice(['Extension activities with higher complexity', 'Independent research opportunities', 'Peer tutoring roles', 'Creative application projects'])}

Struggling Learners:
- {random.choice(['Simplified vocabulary and examples', 'Additional visual supports', 'Extended practice time', 'One-on-one support'])}
- {random.choice(['Graphic organizers', 'Modified assessments', 'Peer partnerships', 'Technology assistance'])}

English Language Learners:
- {random.choice(['Visual vocabulary supports', 'Native language resources when available', 'Collaborative language opportunities', 'Multiple representation methods'])}

Students with IEPs/504 Plans:
- Implementation of individual accommodation plans
- {random.choice(['Extended time', 'Alternative assessment formats', 'Assistive technology', 'Modified expectations as needed'])}

TECHNOLOGY INTEGRATION:
- {random.choice(['Digital collaboration tools', 'Interactive simulations', 'Online research resources', 'Multimedia presentations'])}
- Alignment with Utah Digital Teaching and Learning Standards

HOMEWORK/EXTENSION:
- {random.choice(['Practice problems aligned to lesson objectives', 'Reading assignment with reflection questions', 'Family interview or community connection', 'Preparation for next lesson'])}

POST-LESSON REFLECTION:
What worked well: ________________
Student understanding evidence: ________________
Areas for improvement: ________________
Next lesson adjustments: ________________

Utah Core Standards compliance verified ✓
"""

    elif format_type == "utah_core_guide":
        return f"""UTAH CORE GUIDE LESSON PLAN

Subject: {subject_area} | Grade: {grade_levels} | Date: {lesson_date.strftime('%m/%d/%Y')}
Teacher: {student_name} | School: {school_name} | Class Size: {class_size}

STANDARD: {topic_info['standard']}
{topic_info['description']}

CONCEPTS AND SKILLS TO MASTER:
- {random.choice(['Understand and apply key concepts of', 'Demonstrate proficiency in', 'Analyze and evaluate', 'Create and construct'])} {topic_info['topic'].lower()}
- {random.choice(['Use appropriate academic vocabulary', 'Connect to real-world applications', 'Employ multiple problem-solving strategies', 'Collaborate effectively with peers'])}
- {random.choice(['Explain reasoning and thinking', 'Make connections to prior learning', 'Transfer skills to new situations', 'Demonstrate conceptual understanding'])}

TEACHER BACKGROUND INFORMATION:
This lesson builds on students' prior understanding of {random.choice(['foundational concepts', 'prerequisite skills', 'related topics', 'basic principles'])} and prepares them for {random.choice(['advanced applications', 'future learning', 'complex problem-solving', 'higher-order thinking'])}. Key considerations include {random.choice(['developmental appropriateness', 'cultural responsiveness', 'individual learning needs', 'misconception awareness'])}.

CRITICAL BACKGROUND KNOWLEDGE:
Students should have prior experience with:
- {random.choice(['Basic computational skills', 'Fundamental reading strategies', 'Scientific method steps', 'Historical thinking concepts'])}
- {random.choice(['Collaborative work strategies', 'Academic discussion norms', 'Technology tool usage', 'Safety procedures'])}

ACADEMIC VOCABULARY:
Primary terms: {random.choice(['analyze, evaluate, synthesize', 'compare, contrast, classify', 'predict, infer, conclude', 'organize, sequence, categorize'])}
Supporting terms: {random.choice(['data, evidence, pattern', 'cause, effect, relationship', 'structure, function, system', 'perspective, context, significance'])}

SUGGESTED MODELS:
{random.choice(['Hands-on manipulatives', 'Digital simulations', 'Graphic organizers', 'Physical demonstrations'])}

SUGGESTED STRATEGIES:
- {random.choice(['Think-pair-share discussions', 'Hands-on manipulative use', 'Graphic organizer completion', 'Digital tool integration'])}
- {random.choice(['Questioning techniques for deeper thinking', 'Scaffolded practice opportunities', 'Multiple representation methods', 'Real-world connection activities'])}

LESSON ACTIVITIES:

Opening Activity (10 minutes):
{random.choice(['Students examine real-world examples', 'Review and connect to previous learning', 'Engage with thought-provoking questions', 'Analyze visual or multimedia resources'])} related to {topic_info['topic']}

Main Activity (25 minutes):
{random.choice(['Collaborative investigation using hands-on materials', 'Guided practice with immediate feedback', 'Problem-solving in small groups', 'Digital simulation or interactive activity'])}. Students will {random.choice(['collect and analyze data', 'construct explanations', 'develop models or representations', 'evaluate different perspectives'])}.

Closing Activity (10 minutes):
{random.choice(['Students summarize key learnings', 'Share solutions and strategies', 'Connect to broader concepts', 'Preview upcoming learning'])}

ASSESSMENT EVIDENCE:
- {random.choice(['Student work samples', 'Observation notes', 'Self-assessment reflections', 'Peer feedback'])}
- {random.choice(['Formative check questions', 'Exit ticket responses', 'Discussion participation', 'Problem-solving approaches'])}

MATERIALS AND RESOURCES:
- Utah Core Standards-aligned materials
- {random.choice(['Interactive technology tools', 'Hands-on manipulatives', 'Primary source documents', 'Scientific equipment'])}
- {random.choice(['Graphic organizers', 'Assessment rubrics', 'Reference materials', 'Digital resources'])}

This lesson aligns with Utah Core Standards and supports student achievement of grade-level expectations.
"""

    elif format_type == "uen_format":
        return f"""UEN LESSON PLAN
Utah Education Network Standards-Aligned Instruction

LESSON IDENTIFICATION:
Title: {topic_info['topic']}
Subject: {subject_area}
Grade Level: {grade_levels}
Duration: {random.choice(['One 50-minute period', 'One 45-minute period', 'Two 30-minute sessions'])}
Teacher: {student_name}
School: {school_name}
Date: {lesson_date.strftime('%B %d, %Y')}

UTAH CORE STANDARDS:
Primary Standard: {topic_info['standard']} - {topic_info['description']}
Supporting Standards: {random.choice(['Mathematical Practices 1-8', 'Science and Engineering Practices', 'ELA Standards for Literacy', 'Social Studies Thinking Standards'])}

LESSON OVERVIEW:
Students will explore {topic_info['topic'].lower()} through {random.choice(['inquiry-based learning', 'collaborative problem-solving', 'hands-on investigation', 'multimedia analysis'])}. This lesson connects to {random.choice(['real-world applications', 'student experiences', 'cross-curricular themes', 'community connections'])} and supports development of {random.choice(['critical thinking', 'communication skills', 'problem-solving abilities', 'collaborative competencies'])}.

LEARNING OBJECTIVES:
By the end of this lesson, students will be able to:
1. {topic_info['description']}
2. {random.choice(['Communicate understanding using appropriate vocabulary', 'Apply concepts to solve authentic problems', 'Collaborate effectively with diverse perspectives', 'Demonstrate learning through multiple modalities'])}
3. {random.choice(['Make connections to prior and future learning', 'Evaluate the effectiveness of different strategies', 'Create original examples or applications', 'Reflect on their learning process'])}

PREREQUISITE KNOWLEDGE:
Students should have prior understanding of:
- {random.choice(['Basic concepts from previous units', 'Fundamental skills in the subject area', 'Academic vocabulary and terminology', 'Collaborative learning expectations'])}

MATERIALS:
- {random.choice(['Interactive whiteboard or projector', 'Student devices (tablets/laptops)', 'Manipulatives or hands-on materials', 'Laboratory equipment'])}
- {random.choice(['Printed handouts and graphic organizers', 'Digital resources and simulations', 'Reference materials and texts', 'Assessment tools and rubrics'])}
- UEN digital resources: {random.choice(['eMedia content library', "Utah's Online School Library", 'Interactive learning modules', 'Virtual field trip resources'])}

INSTRUCTIONAL PROCEDURES:

Hook/Anticipatory Set (8 minutes):
{random.choice(['Present intriguing question or scenario', 'Show engaging multimedia content', 'Demonstrate surprising phenomenon', 'Share real-world connection'])} to capture student interest and activate prior knowledge about {topic_info['topic']}.

Instruction/Modeling (15 minutes):
{random.choice(['Guide students through key concepts using interactive demonstration', 'Model problem-solving strategies with student input', 'Facilitate discovery through structured inquiry', 'Present information using multiple modalities'])}. Emphasize {random.choice(['conceptual understanding', 'strategic thinking', 'vocabulary development', 'procedural fluency'])}.

Guided Practice (15 minutes):
Students work in {random.choice(['collaborative pairs', 'small groups of 3-4', 'flexible groupings'])} to {random.choice(['solve problems with teacher support', 'investigate questions using provided materials', 'analyze examples and non-examples', 'complete structured practice activities'])}. Teacher circulates to provide feedback and support.

Independent Practice (8 minutes):
Students {random.choice(['complete individual application problems', 'create their own examples', 'solve challenge questions', 'begin homework assignment'])} to demonstrate understanding.

Closure (4 minutes):
{random.choice(['Students share key learnings and insights', 'Review lesson objectives and assess achievement', 'Preview connections to upcoming learning', 'Complete exit ticket or reflection prompt'])}

ASSESSMENT:
Formative Assessment:
- {random.choice(['Observation during collaborative work', 'Check for understanding questions', 'Student response systems', 'Peer discussions and sharing'])}
- {random.choice(['Work sample analysis', 'Quick writes or sketches', 'Thumbs up/down comprehension checks', 'One question, one connection, one reflection'])}

Summative Assessment:
- {random.choice(['End-of-unit test questions', 'Performance-based task', 'Portfolio evidence', 'Project component'])}

ACCOMMODATIONS AND MODIFICATIONS:
- {random.choice(['Extended time for processing', 'Alternative response formats', 'Visual and auditory supports', 'Simplified language and instructions'])}
- {random.choice(['Flexible grouping arrangements', 'Technology assistance', 'Modified assignments', 'Additional practice opportunities'])}
- {random.choice(['Enrichment activities for advanced learners', 'ELL supports and translations', 'IEP/504 plan accommodations', 'Multi-sensory learning options'])}

TECHNOLOGY INTEGRATION:
This lesson incorporates {random.choice(['UEN digital resources', 'interactive simulations', 'collaborative online tools', 'multimedia presentations'])} to enhance learning and support Utah's Digital Teaching and Learning Standards.

EXTENSION ACTIVITIES:
- {random.choice(['Research project connections', 'Home and community applications', 'Cross-curricular investigations', 'Service learning opportunities'])}
- {random.choice(['Creative expression projects', 'Peer teaching opportunities', 'Advanced problem-solving challenges', 'Real-world internship connections'])}

REFLECTION:
Post-lesson teacher reflection questions:
1. How effectively did students meet the learning objectives?
2. What evidence supports student understanding?
3. What adjustments would improve this lesson?
4. How will this lesson inform future instruction?

Lesson plan developed using UEN resources and aligned with Utah Core Standards.
© Utah Education Network - Supporting Utah educators and students
"""

    else:  # usbe_template format
        return f"""UTAH STATE BOARD OF EDUCATION
Lesson Plan Template

TEACHER INFORMATION:
Name: {student_name}
School: {school_name}
Subject: {subject_area}
Grade(s): {grade_levels}
Class Period: {random.choice(['1st Period', '2nd Period', '3rd Period', '4th Period', 'Block Schedule'])}
Date: {lesson_date.strftime('%m/%d/%Y')}
Class Size: {class_size} students

STANDARDS AND OBJECTIVES:
Utah Core Standard: {topic_info['standard']}
Standard Description: {topic_info['description']}

Cross-Curricular Connections: {random.choice(['Mathematical reasoning and problem-solving', 'Scientific inquiry and investigation', 'Historical thinking and analysis', 'Literary analysis and communication'])}

Learning Objectives (Students will...):
• {topic_info['description']}
• {random.choice(['Demonstrate understanding through multiple assessment methods', 'Apply learning to authentic, real-world situations', 'Collaborate respectfully with diverse groups', 'Communicate ideas clearly using academic language'])}
• {random.choice(['Reflect on learning progress and set goals', 'Make connections between current and prior learning', 'Transfer knowledge to new and novel situations', 'Evaluate the effectiveness of different approaches'])}

LESSON COMPONENTS:

Anticipatory Set/Hook (5-10 minutes):
Purpose: {random.choice(['Activate prior knowledge and create interest', 'Establish learning context and relevance', 'Preview key concepts and vocabulary', 'Connect to student experiences and interests'])}
Activity: {random.choice(['Engaging question or problem scenario', 'Multimedia presentation or demonstration', 'Think-pair-share discussion', 'Hands-on exploration or investigation'])}

Instruction and Modeling (15-20 minutes):
Teaching Strategy: {random.choice(['Direct instruction with interactive elements', 'Inquiry-based discovery learning', 'Collaborative investigation and discussion', 'Technology-enhanced presentation'])}
Content Delivery: {random.choice(['Step-by-step modeling with student participation', 'Guided discovery through questioning', 'Multiple examples with non-examples', 'Visual, auditory, and kinesthetic approaches'])}
Key Vocabulary: {random.choice(['Terms introduced in context with visual supports', 'Academic language explicitly taught and practiced', 'Vocabulary connections to prior learning', 'Student-friendly definitions and examples'])}

Guided Practice (15-20 minutes):
Student Activity: {random.choice(['Collaborative problem-solving in small groups', 'Structured practice with teacher feedback', 'Hands-on investigation with data collection', 'Digital simulation or interactive activity'])}
Teacher Role: {random.choice(['Facilitate and provide targeted support', 'Monitor understanding and address misconceptions', 'Ask probing questions to deepen thinking', 'Differentiate support based on student needs'])}

Independent Practice (5-10 minutes):
Application: {random.choice(['Individual problem-solving or creation task', 'Silent practice with immediate feedback', 'Portfolio work or journal reflection', 'Begin homework or extended project'])}

Closure (3-5 minutes):
Summarizing Activity: {random.choice(['Student explanation of key learnings', 'Quick review of lesson objectives', 'Preview of upcoming connections', 'Exit ticket or reflection prompt'])}

ASSESSMENT PLAN:
Formative Assessment Methods:
- {random.choice(['Questioning strategies during instruction', 'Observation of student work and discussions', 'Quick check-ins and thumbs up/down', 'Digital polling or response systems'])}
- {random.choice(['Student self-assessment and goal setting', 'Peer feedback and collaboration', 'Work sample analysis and feedback', 'Learning log or journal entries'])}

Summative Assessment Connections:
- {random.choice(['Unit test questions aligned to objectives', 'Performance task or authentic assessment', 'Portfolio collection and reflection', 'Project-based evaluation'])}

Success Criteria:
Students will demonstrate mastery when they can:
• {random.choice(['Explain concepts using appropriate vocabulary', 'Apply skills to solve novel problems', 'Teach concepts to a peer effectively', 'Create original examples or applications'])}
• {random.choice(['Score proficient on assessment rubric', 'Meet individual learning goals', 'Show growth from baseline measures', 'Transfer learning to new contexts'])}

DIFFERENTIATION STRATEGIES:
Content Modifications:
- {random.choice(['Multiple complexity levels available', 'Various entry points for different learners', 'Alternative texts and resources', 'Supplementary materials for support'])}

Process Variations:
- {random.choice(['Flexible grouping arrangements', 'Choice in learning activities', 'Various pacing options', 'Multiple learning modalities'])}

Product Options:
- {random.choice(['Alternative ways to demonstrate learning', 'Technology-enhanced presentations', 'Creative expression opportunities', 'Portfolio-based evidence'])}

Specific Accommodations:
- IEP/504 accommodations implemented as specified
- {random.choice(['Extended time and processing breaks', 'Alternative assessment formats', 'Assistive technology support', 'Modified complexity levels'])}
- {random.choice(['ELL supports with visual aids', 'Native language resources when available', 'Collaborative language opportunities', 'Simplified directions and examples'])}

MATERIALS AND RESOURCES:
Instructional Materials:
- {random.choice(['Utah Core Standards-aligned textbooks', 'Digital resources and online tools', 'Hands-on manipulatives and equipment', 'Primary source documents'])}
- {random.choice(['Interactive whiteboard technology', 'Student response systems', 'Laboratory or art supplies', 'Reference materials and dictionaries'])}

Technology Integration:
- Platform: {random.choice(['Google Classroom', 'Canvas LMS', 'Seesaw', 'Schoology'])}
- Tools: {random.choice(['Interactive simulations', 'Collaborative documents', 'Digital creation tools', 'Assessment platforms'])}

Utah Resources:
- {random.choice(['UEN digital content library', "Utah's Online School Library", 'State museum virtual tours', 'Local community partnerships'])}

SAFETY CONSIDERATIONS:
- {random.choice(['Laboratory safety procedures reviewed', 'Physical movement space established', 'Technology use guidelines followed', 'Emergency procedures accessible'])}
- {random.choice(['Student allergy and health considerations', 'Supervision protocols for group work', 'Material handling safety measures', 'Emotional safety and respect norms'])}

HOMEWORK/EXTENSION:
Assignment: {random.choice(['Practice problems aligned to lesson objectives', 'Reading and reflection questions', 'Research or investigation project', 'Family interview or community connection'])}
Purpose: {random.choice(['Reinforce and extend classroom learning', 'Prepare for upcoming instruction', 'Connect learning to home and community', 'Develop independent learning skills'])}

REFLECTION AND NEXT STEPS:
Post-Lesson Evaluation:
1. Objective Achievement: ________________
2. Student Engagement Evidence: ________________
3. Assessment Data Analysis: ________________
4. Instructional Adjustments Needed: ________________
5. Follow-up Learning Plan: ________________

Professional Growth Connections:
- {random.choice(['Collaboration with grade-level team', 'Data analysis with instructional coach', 'Professional learning community discussion', 'Mentoring conversation topics'])}

This lesson plan aligns with Utah State Board of Education standards and supports the mission of preparing students for success in an increasingly complex world.

✓ Utah Core Standards Aligned
✓ USBE Guidelines Followed  
✓ Assessment Plan Integrated
✓ Differentiation Strategies Included
""" 