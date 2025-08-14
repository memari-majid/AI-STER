"""
Rubric data for AI-STER evaluation system

Copyright © 2025 Utah Valley University School of Education
All Rights Reserved.

This software is proprietary and confidential property of Utah Valley University
School of Education. Licensed for educational use only.

Converted from markdown files to structured Python data
"""

def get_field_evaluation_items():
    """Get Field Evaluation rubric items (3-week field experience)"""
    return [
        {
            'id': 'LL3',
            'code': 'LL3',
            'title': 'Strengthen and support classroom norms that encourage positive teacher-student and student-student relationships.',
            'context': 'Observation',
            'competency_area': 'Learners and Learning',
            'type': 'Application competency',
            'levels': {
                '0': 'Does not demonstrate awareness of classroom norms.',
                '1': 'Demonstrates understanding of the norms of the classroom (e.g. behavioral, instructional, procedural).',
                '2': '…and implements classroom norms that encourage positive teacher-student and student-student relationships.',
                '3': '… and Actively creates and sustains classroom norms in which teacher-student and student-student relationships are positive.'
            }
        },
        {
            'id': 'LL5',
            'code': 'LL5',
            'title': 'Communicate clear expectations and procedures that include positive behavior interventions to promote student ownership of behavior.',
            'context': 'Observation',
            'competency_area': 'Learners and Learning',
            'type': 'Demonstration competency',
            'levels': {
                '0': 'Does not communicate clear expectations AND does not use positive reinforcements.',
                '1': 'Communicates expectations OR uses positive reinforcements.',
                '2': 'Communicates clear expectations and procedures, including positive behavior interventions.',
                '3': '…and Creates opportunities for students to self-monitor their behavior.'
            }
        },
        {
            'id': 'IC1_IC2',
            'code': 'IC1/IC2',
            'title': 'Demonstrate an understanding of Utah Core Standards. Create learning intentions and success criteria that are aligned to Utah Core Standards.',
            'context': 'Observation or Conference w/MT and ST',
            'competency_area': 'Instructional Clarity',
            'type': 'Demonstration competency',
            'levels': {
                '0': 'Does not demonstrate an understanding of Utah Core Standards. Lesson intentions and success criteria are missing or not aligned to Utah Core Standards.',
                '1': 'Demonstrates inconsistent understanding of Utah Core Standards. OR Creates lesson intentions and success criteria that are inconsistently aligned to Utah Core Standards.',
                '2': 'Demonstrates consistent understanding of Utah Core Standards AND Creates learning intentions and success criteria that are consistently aligned to Utah Core Standards.',
                '3': '…and Meaningfully integrates content that aligns with Utah Core Standards.'
            }
        },
        {
            'id': 'CC2',
            'code': 'CC2',
            'title': 'Promote a classroom environment in which students will respect and value each other.',
            'context': 'Observation',
            'competency_area': 'Classroom Climate',
            'type': 'Application competency',
            'levels': {
                '0': 'Creates a classroom environment in which students are disrespectful.',
                '1': 'Creates a classroom environment where the teacher conveys respect for students.',
                '2': '… and Creates a classroom environment in which students respect and value each other.',
                '3': '…and Explicitly teaches students to respect and value each other.'
            }
        },
        {
            'id': 'CC3',
            'code': 'CC3',
            'title': 'Involve students in establishing clear guidelines for behavior.',
            'context': 'Observation AND Conference w/MT',
            'competency_area': 'Classroom Climate',
            'type': 'Application competency',
            'levels': {
                '0': 'Does not establish clear guidelines for behavior.',
                '1': 'Establishes clear guidelines for behavior.',
                '2': '…and Involves students in establishing clear guidelines for behavior.',
                '3': '…and Meaningfully involves students in the ownership of action steps and guidelines for subsequent behavior.'
            }
        },
        {
            'id': 'CC4',
            'code': 'CC4',
            'title': 'Address physical and emotional safety concerns in a timely manner.',
            'context': 'Observation AND Conference w/MT',
            'competency_area': 'Classroom Climate',
            'type': 'Application competency',
            'levels': {
                '0': 'Does not address physical and emotional safety concerns.',
                '1': 'Shows awareness of physical and emotional safety concerns.',
                '2': '…and Addresses physical and emotional safety concerns in a timely manner.',
                '3': '…and Creates an environment that proactively addresses physical and emotional safety concerns.'
            }
        },
        {
            'id': 'CC6',
            'code': 'CC6',
            'title': 'Strategically organize and structure the classroom environment for optimal student learning.',
            'context': 'Observation',
            'competency_area': 'Classroom Climate',
            'type': 'Application competency',
            'levels': {
                '0': 'Fails to use classroom management strategies.',
                '1': 'Uses classroom management strategies.',
                '2': '…and Strategically organizes and structures the classroom environment for optimal student learning, including use of instructional and classroom management strategies that promote student learning.',
                '3': '...and Manages time, space, and attention to increase participation.'
            }
        },
        {
            'id': 'CC8',
            'code': 'CC8',
            'title': 'Encourage an environment where students feel safe to take risks, participate and engage.',
            'context': 'Observation',
            'competency_area': 'Classroom Climate',
            'type': 'Application competency',
            'levels': {
                '0': 'Creates an environment in which students feel unsafe.',
                '1': 'Creates an environment in which most students participate.',
                '2': '…and Creates an environment in which students feel safe to participate and engage.',
                '3': '…and Creates an environment in which students are encouraged to take risks as part of the learning process.'
            }
        }
    ]

def get_ster_items():
    """Get STER rubric items (comprehensive summative assessment)"""
    return [
        # LEARNERS AND LEARNING (7 items total: LL1-LL7)
        {
            'id': 'LL1',
            'code': 'LL1',
            'title': 'Participate in meetings with student\'s parents/guardians (e.g., IEP, 504, behavior, attendance, parent teacher conferences) to help assess and plan needed student support.',
            'context': 'Conference w/MT',
            'competency_area': 'Learners and Learning',
            'type': 'Demonstration competency',
            'evaluator_role': 'cooperating_teacher',  # Cream row - for cooperating teachers
            'levels': {
                '0': 'Works in isolation and does not collaborate with students\' parents/guardians.',
                '1': 'Considers input from students\' parents/guardians.',
                '2': '…and Participates in a meeting with parents/guardians under mentor supervision.',
                '3': '…and Initiates communication with parents/guardians to design supports that meet the specific needs of students.'
            },
            'example_justification': 'The student teacher demonstrates a strong commitment to foster positive relationships with students\' families by actively considering input from parents and guardians. This was particularly evident during an IEP meeting with parents/guardians, conducted under mentor supervision, where the student teacher engaged in meaningful discussions, listened attentively, and incorporated feedback into their instructional approach.'
        },
        {
            'id': 'LL2',
            'code': 'LL2',
            'title': 'Design learning that builds on the learner\'s background knowledge and supports students\' needs.',
            'context': 'Observation',
            'competency_area': 'Learners and Learning',
            'type': 'Application competency',
            'levels': {
                '0': 'Lacks awareness of learners\' background knowledge. Lacks awareness of developmental needs.',
                '1': 'Demonstrates awareness of learners\' background knowledge and needs (e.g. learners\' names, contextual information).',
                '2': '...and Designs learning experiences that reflect understanding of learners\' academic background knowledge.',
                '3': '...and Implements and modifies learning experiences based on specific learners\' developmental levels.'
            },
            'example_justification': 'The student teacher demonstrates a keen awareness of learners\' background knowledge and individual needs by taking the time to learn students\' names and gather relevant contextual information about their academic and personal experiences. This understanding is reflected in the thoughtfully designed learning experiences, which are tailored to align with the students\' prior knowledge and unique learning profiles.'
        },
        {
            'id': 'LL3',
            'code': 'LL3',
            'title': 'Strengthen and support classroom norms that encourage positive teacher-student and student-student relationships.',
            'context': 'Observation',
            'competency_area': 'Learners and Learning',
            'type': 'Application competency',
            'levels': {
                '0': 'Does not demonstrate awareness of classroom norms.',
                '1': 'Demonstrates understanding of the norms of the classroom (e.g. behavioral, instructional, procedural).',
                '2': '…and Implements classroom norms that encourage positive teacher-student and student-student relationships.',
                '3': '… and Actively creates and sustains classroom norms in which teacher-student and student-student relationships are positive.'
            },
            'example_justification': 'The student teacher demonstrates a solid understanding of the classroom norms, including behavioral, instructional, and procedural expectations, which contribute to a well-managed learning environment. They effectively implement these norms in a way that fosters positive relationships between the teacher and students, as well as among peers.'
        },
        {
            'id': 'LL4',
            'code': 'LL4',
            'title': 'Identify adaptations made to instruction to benefit learners of varied backgrounds.',
            'context': 'Observation',
            'competency_area': 'Learners and Learning',
            'type': 'Application competency',
            'levels': {
                '0': 'Does not adapt instruction for learners of varied backgrounds.',
                '1': 'Plans adaptations that may or may not be appropriate for the learners in the classroom, e.g., generic adaptations such as providing more time.',
                '2': 'Plans and implements appropriate adaptations for learners.',
                '3': 'Plans appropriate adaptations for learners AND adjusts instruction based on developmental, cultural, or linguistic needs of the students.'
            },
            'example_justification': 'The student teacher effectively plans and implements adaptations that are well-suited to the diverse needs of learners in the classroom. They thoughtfully craft support to individual student\'s needs, fostering greater engagement and accessibility to the curriculum.'
        },
        {
            'id': 'LL5',
            'code': 'LL5',
            'title': 'Communicate clear expectations and procedures that include positive behavior interventions to promote student ownership of behavior.',
            'context': 'Observation',
            'competency_area': 'Learners and Learning',
            'type': 'Demonstration competency',
            'levels': {
                '0': 'Does not communicate clear expectations AND does not use positive reinforcements.',
                '1': 'Communicates expectations OR uses positive reinforcements.',
                '2': 'Communicates clear expectations and procedures, including positive behavior interventions.',
                '3': '…and Creates opportunities for students to self-monitor their behavior.'
            },
            'example_justification': 'The student teacher consistently communicates clear expectations and procedures, establishing a structured and positive learning environment. By articulating rules and routines effectively, they help students understand classroom expectations and foster a sense of predictability.'
        },
        {
            'id': 'LL6',
            'code': 'LL6',
            'title': 'Encourage student ownership of learning by applying real world connection and authentic learning experiences in the classroom.',
            'context': 'Observation',
            'competency_area': 'Learners and Learning',
            'type': 'Application competency',
            'levels': {
                '0': 'Sources and learning experiences are not appropriate for learning intentions.',
                '1': 'Uses sources of information appropriate to content area, but the sources and learning experiences lack a real-world connection (e.g., textbook-centered).',
                '2': 'Uses appropriate sources of information and designs learning experiences that demonstrate a real-world connection (e.g., realia, authentic media, engagement with community).',
                '3': '… and Engages learners in using multiple, appropriate sources of information that foster student ownership of authentic learning experiences through a real-world connection.'
            },
            'example_justification': 'The student teacher thoughtfully integrates appropriate sources of information and designs learning experiences that connect classroom content to the real world, enhancing student engagement and relevance.'
        },
        {
            'id': 'LL7',
            'code': 'LL7',
            'title': 'Provide formative and timely feedback to guide students in self-assessment of learning.',
            'context': 'Observation',
            'competency_area': 'Learners and Learning',
            'type': 'Demonstration competency',
            'levels': {
                '0': 'Does not provide feedback to students.',
                '1': 'Provides general feedback, e.g. "good job".',
                '2': 'Provides specific and timely feedback and encourages students to apply it to future performance.',
                '3': '….and Structures opportunities for students to apply feedback to improve their learning and self-assessment of progress towards learning goals.'
            },
            'example_justification': 'The student teacher consistently provides specific, constructive, and timely feedback that addresses students\' individual strengths and areas for improvement. This feedback is clear and actionable, allowing students to understand exactly how they can enhance their work.'
        },
        
        # INSTRUCTIONAL CLARITY (5 items total: IC1/IC2, IC3, IC4, IC5/IC6, IC7)
        {
            'id': 'IC1_IC2',
            'code': 'IC1/IC2',
            'title': 'Demonstrate an understanding of Utah Core Standards and create learning intentions and success criteria that are aligned to Utah Core Standards.',
            'context': 'Observation or Conference w/MT and ST',
            'competency_area': 'Instructional Clarity',
            'type': 'Demonstration competency',
            'levels': {
                '0': 'Does not demonstrate an understanding of Utah Core Standards. Lesson intentions and success criteria are missing or not aligned to Utah Core Standards.',
                '1': 'Demonstrates inconsistent understanding of Utah Core Standards OR creates lesson intentions and success criteria that are inconsistently aligned to Utah Core Standards.',
                '2': 'Demonstrates consistent understanding of Utah Core Standards AND creates learning intentions and success criteria that are consistently aligned to Utah Core Standards.',
                '3': '…and Meaningfully integrates content that aligns with Utah Core Standards.'
            }
        },
        {
            'id': 'IC3',
            'code': 'IC3',
            'title': 'Design learning experiences aligned to learning intentions and success criteria.',
            'context': 'Observation or Conference w/MT and ST',
            'competency_area': 'Instructional Clarity',
            'type': 'Demonstration competency',
            'levels': {
                '0': 'No evidence of learning objectives/intentions in design of learning experiences.',
                '1': 'Inconsistently provides evidence of learning objectives/intentions or success criteria in lesson plans.',
                '2': 'Designs learning experiences that are aligned to learning intentions and success criteria.',
                '3': '…and Uses students\' response to instruction to inform future lessons.'
            },
            'example_justification': 'The student teacher effectively designs learning experiences that are well-aligned with clearly defined learning intentions and success criteria. Each activity and task is purposefully selected to directly support students in achieving the lesson\'s goals.'
        },
        {
            'id': 'IC4',
            'code': 'IC4',
            'title': 'Plan learning progressions that build upon students\' previous learning and support current learning intentions.',
            'context': 'Observation or Conference w/MT and ST',
            'competency_area': 'Instructional Clarity',
            'type': 'Application competency',
            'levels': {
                '0': 'Lesson plans are not appropriate for the age of students or grade level.',
                '1': 'Lesson plans are appropriate for the age of students or grade level including cursory evidence of previous learning.',
                '2': '…and Lesson plans are built upon previous evidence of learning and support current learning intentions.',
                '3': '…and Lesson plans extend previous learning and are flexibly adjusted to provide appropriate challenges.'
            }
        },
        {
            'id': 'IC5_IC6',
            'code': 'IC5/IC6',
            'title': 'Provide opportunities for students to track, reflect on, and set goals for their learning and allow students multiple opportunities and means for demonstration of competency.',
            'context': 'Observation',
            'competency_area': 'Instructional Clarity',
            'type': 'Demonstration competency',
            'levels': {
                '0': 'Does not provide opportunities for students to track, reflect on, or set goals for their learning. Does not provide opportunities for students to demonstrate competency.',
                '1': 'Provides infrequent opportunities for students to track, reflect on, OR set goals for their learning. Provides one teacher-selected means for students to demonstrate competency.',
                '2': 'Provides opportunities for students to track, reflect on, and set goals for their learning AND allows multiple opportunities for demonstrating competency.',
                '3': '…and Guides students in analyzing their own learning and setting their own goals AND guides students in selecting appropriate means to demonstrate competency.'
            }
        },
        {
            'id': 'IC7',
            'code': 'IC7',
            'title': 'Design a variety of instructional strategies to engage students and promote active learning.',
            'context': 'Observation or Conference w/MT and ST',
            'competency_area': 'Instructional Clarity',
            'type': 'Application competency',
            'levels': {
                '0': 'Does not engage students or promote active learning.',
                '1': 'Uses a limited range of instructional strategies.',
                '2': 'Designs a variety of instructional strategies to engage students and promote active learning.',
                '3': '…and Implements instructional strategies that are responsive to students\' progress toward learning intentions.'
            }
        },
        
        # INSTRUCTIONAL PRACTICE (8 items total: IP1-IP8)
        {
            'id': 'IP1',
            'code': 'IP1',
            'title': 'Include differentiated strategies aligned with lesson objectives to meet the unique needs of every student.',
            'context': 'Observation',
            'competency_area': 'Instructional Practice',
            'type': 'Application competency',
            'levels': {
                '0': 'Does not include differentiated strategies.',
                '1': 'Includes limited differentiated strategies.',
                '2': 'Includes differentiated strategies aligned with lesson objectives to meet student needs.',
                '3': '…and Flexibly adjusts differentiated strategies based on student responses.'
            }
        },
        {
            'id': 'IP2',
            'code': 'IP2',
            'title': 'Provide appropriate strategies to promote and facilitate students\' problem solving, critical thinking, and discourse.',
            'context': 'Observation',
            'competency_area': 'Instructional Practice',
            'type': 'Application competency',
            'levels': {
                '0': 'Does not provide strategies to promote problem solving, critical thinking, or discourse.',
                '1': 'Provides limited strategies to promote problem solving, critical thinking, or discourse.',
                '2': 'Provides appropriate strategies to promote and facilitate students\' problem solving, critical thinking, and discourse.',
                '3': '…and Creates multiple opportunities for students to engage in higher-order thinking and meaningful discourse.'
            }
        },
        {
            'id': 'IP3',
            'code': 'IP3',
            'title': 'Analyze student assessment data, including both formative and summative assessments, to inform and adjust instruction.',
            'context': 'Observation or Conference w/MT and ST',
            'competency_area': 'Instructional Practice',
            'type': 'Application competency',
            'levels': {
                '0': 'Does not analyze assessment data.',
                '1': 'Collects assessment data but does not analyze it to inform instruction.',
                '2': 'Analyzes assessment data to inform and adjust instruction.',
                '3': '…and Uses data analysis to modify instruction in real-time based on student needs.'
            }
        },
        {
            'id': 'IP4',
            'code': 'IP4',
            'title': 'Employ a variety of assessments that allow all students to demonstrate learning.',
            'context': 'Observation',
            'competency_area': 'Instructional Practice',
            'type': 'Application competency',
            'levels': {
                '0': 'Does not employ variety in assessments.',
                '1': 'Employs limited variety in assessments.',
                '2': 'Employs a variety of assessments that allow all students to demonstrate learning.',
                '3': '…and Provides choice in assessment formats based on student needs and preferences.'
            }
        },
        {
            'id': 'IP5',
            'code': 'IP5',
            'title': 'Provide feedback to students and parents that supports learning and growth.',
            'context': 'Observation or Conference w/MT and ST',
            'competency_area': 'Instructional Practice',
            'type': 'Demonstration competency',
            'levels': {
                '0': 'Does not provide meaningful feedback.',
                '1': 'Provides general feedback to students.',
                '2': 'Provides specific feedback to students and parents that supports learning and growth.',
                '3': '…and Collaborates with students to set personalized learning goals based on feedback.'
            }
        },
        {
            'id': 'IP6',
            'code': 'IP6',
            'title': 'Provide relevant learning opportunities that are grounded in student interests, needs, and backgrounds.',
            'context': 'Observation',
            'competency_area': 'Instructional Practice',
            'type': 'Application competency',
            'levels': {
                '0': 'Does not provide relevant learning opportunities.',
                '1': 'Provides limited relevant learning opportunities.',
                '2': 'Provides relevant learning opportunities grounded in student interests, needs, and backgrounds.',
                '3': '…and Regularly incorporates student voice and choice in designing learning opportunities.'
            }
        },
        {
            'id': 'IP7',
            'code': 'IP7',
            'title': 'Encourage students to think about, engage with, and access content in creative ways.',
            'context': 'Observation',
            'competency_area': 'Instructional Practice',
            'type': 'Application competency',
            'levels': {
                '0': 'Does not encourage creative engagement with content.',
                '1': 'Provides limited opportunities for creative engagement.',
                '2': 'Encourages students to think about, engage with, and access content in creative ways.',
                '3': '…and Facilitates student-led creative exploration and innovation.'
            }
        },
        {
            'id': 'IP8',
            'code': 'IP8',
            'title': 'Intentionally select tools and technology to design and implement activities that promote active student technology use.',
            'context': 'Observation',
            'competency_area': 'Instructional Practice',
            'type': 'Application competency',
            'levels': {
                '0': 'Does not use technology or uses it inappropriately.',
                '1': 'Uses technology in limited ways.',
                '2': 'Intentionally selects tools and technology to promote active student technology use.',
                '3': '…and Empowers students to select and use technology tools for learning and creation.'
            }
        },
        
        # CLASSROOM CLIMATE (8 items total: CC1-CC8)
        {
            'id': 'CC1',
            'code': 'CC1',
            'title': 'Create a learning climate that is sensitive to multiple experiences and backgrounds, including trauma informed practices and restorative practices.',
            'context': 'Observation',
            'competency_area': 'Classroom Climate',
            'type': 'Demonstration competency',
            'levels': {
                '0': 'Creates a classroom environment that is insensitive to students\' experiences and backgrounds.',
                '1': 'Creates a learning environment that is sensitive to students\' experiences and backgrounds.',
                '2': 'Creates a learning climate that is sensitive to student experiences and backgrounds AND includes trauma informed and restorative practices.',
                '3': '…and Aligns trauma-informed and restorative practices to students\' backgrounds and experiences.'
            }
        },
        {
            'id': 'CC2',
            'code': 'CC2',
            'title': 'Promote a classroom environment in which students will respect and value each other.',
            'context': 'Observation',
            'competency_area': 'Classroom Climate',
            'type': 'Application competency',
            'levels': {
                '0': 'Creates a classroom environment in which students are disrespectful.',
                '1': 'Creates a classroom environment where the teacher conveys respect for students.',
                '2': '… and Creates a classroom environment in which students respect and value each other.',
                '3': '…and Explicitly teaches students to respect and value each other.'
            }
        },
        {
            'id': 'CC3',
            'code': 'CC3',
            'title': 'Involve students in establishing clear guidelines for behavior.',
            'context': 'Observation AND Conference w/MT',
            'competency_area': 'Classroom Climate',
            'type': 'Application competency',
            'levels': {
                '0': 'Does not establish clear guidelines for behavior.',
                '1': 'Establishes clear guidelines for behavior.',
                '2': '…and Involves students in establishing clear guidelines for behavior.',
                '3': '…and Meaningfully involves students in the ownership of action steps and guidelines for subsequent behavior.'
            }
        },
        {
            'id': 'CC4',
            'code': 'CC4',
            'title': 'Address physical and emotional safety concerns in a timely manner.',
            'context': 'Observation AND Conference w/MT',
            'competency_area': 'Classroom Climate',
            'type': 'Application competency',
            'levels': {
                '0': 'Does not address physical and emotional safety concerns.',
                '1': 'Shows awareness of physical and emotional safety concerns.',
                '2': '…and Addresses physical and emotional safety concerns in a timely manner.',
                '3': '…and Creates an environment that proactively addresses physical and emotional safety concerns.'
            }
        },
        {
            'id': 'CC5',
            'code': 'CC5',
            'title': 'Consistently apply the norms of the classroom to align with schoolwide expectations.',
            'context': 'Observation AND Conference w/MT',
            'competency_area': 'Classroom Climate',
            'type': 'Application competency',
            'levels': {
                '0': 'Does not apply classroom norms or align with schoolwide expectations.',
                '1': 'Inconsistently applies classroom norms or schoolwide expectations.',
                '2': 'Consistently applies classroom norms that align with schoolwide expectations.',
                '3': '…and Helps students understand connections between classroom and schoolwide expectations.'
            }
        },
        {
            'id': 'CC6',
            'code': 'CC6',
            'title': 'Strategically organize and structure the classroom environment for optimal student learning.',
            'context': 'Observation',
            'competency_area': 'Classroom Climate',
            'type': 'Application competency',
            'levels': {
                '0': 'Fails to organize classroom environment effectively.',
                '1': 'Organizes classroom environment with limited effectiveness.',
                '2': 'Strategically organizes and structures classroom environment for optimal student learning.',
                '3': '…and Involves students in organizing and maintaining the learning environment.'
            }
        },
        {
            'id': 'CC7',
            'code': 'CC7',
            'title': 'Model and maintain routines and procedures to encourage a predictable and functional classroom.',
            'context': 'Observation AND Conference w/MT',
            'competency_area': 'Classroom Climate',
            'type': 'Application competency',
            'levels': {
                '0': 'Does not establish or maintain routines and procedures.',
                '1': 'Establishes limited routines and procedures.',
                '2': 'Models and maintains routines and procedures for a predictable and functional classroom.',
                '3': '…and Involves students in developing and maintaining classroom routines and procedures.'
            }
        },
        {
            'id': 'CC8',
            'code': 'CC8',
            'title': 'Encourage an environment where students feel safe to take risks, participate and engage.',
            'context': 'Observation',
            'competency_area': 'Classroom Climate',
            'type': 'Application competency',
            'levels': {
                '0': 'Creates an environment in which students feel unsafe.',
                '1': 'Creates an environment in which most students participate.',
                '2': '…and Creates an environment in which students feel safe to participate and engage.',
                '3': '…and Creates an environment in which students are encouraged to take risks as part of the learning process.'
            }
        },
        
        # PROFESSIONAL RESPONSIBILITY (7 items total: PR1-PR7)
        {
            'id': 'PR1',
            'code': 'PR1',
            'title': 'Understand equal opportunity as outlined in R277-328 by acknowledging that all students are capable of learning.',
            'context': 'Conference w/MT',
            'competency_area': 'Professional Responsibility',
            'type': 'Demonstration competency',
            'levels': {
                '0': 'Does not demonstrate understanding of equal opportunity or belief that all students can learn.',
                '1': 'Demonstrates limited understanding of equal opportunity for student learning.',
                '2': 'Understands equal opportunity and acknowledges that all students are capable of learning.',
                '3': '…and Advocates for equitable learning opportunities for all students.'
            }
        },
        {
            'id': 'PR2',
            'code': 'PR2',
            'title': 'Comply with relevant school, district, and state laws, rules, and policies governing the profession.',
            'context': 'Conference w/MT',
            'competency_area': 'Professional Responsibility',
            'type': 'Demonstration competency',
            'levels': {
                '0': 'Does not comply with professional laws, rules, and policies.',
                '1': 'Shows limited understanding of professional laws, rules, and policies.',
                '2': 'Complies with relevant school, district, and state laws, rules, and policies.',
                '3': '…and Demonstrates leadership in understanding and implementing professional standards.'
            }
        },
        {
            'id': 'PR3',
            'code': 'PR3',
            'title': 'Demonstrates intellectual curiosity and values continuous growth by engaging in professional learning.',
            'context': 'Conference w/MT',
            'competency_area': 'Professional Responsibility',
            'type': 'Demonstration competency',
            'levels': {
                '0': 'Does not engage in professional learning or show intellectual curiosity.',
                '1': 'Shows limited engagement in professional learning.',
                '2': 'Demonstrates intellectual curiosity and engages in professional learning.',
                '3': '…and Seeks out and applies additional professional learning opportunities.'
            }
        },
        {
            'id': 'PR4',
            'code': 'PR4',
            'title': 'Engages in reflective practices that support professional, instructional, and schoolwide improvement.',
            'context': 'Conference w/MT',
            'competency_area': 'Professional Responsibility',
            'type': 'Application competency',
            'levels': {
                '0': 'Does not engage in reflective practices.',
                '1': 'Engages in limited reflective practices.',
                '2': 'Engages in reflective practices that support professional and instructional improvement.',
                '3': '…and Uses reflection to contribute to schoolwide improvement initiatives.'
            }
        },
        {
            'id': 'PR5',
            'code': 'PR5',
            'title': 'Use effective communication with students, parents, and colleagues about student learning.',
            'context': 'Conference w/MT',
            'competency_area': 'Professional Responsibility',
            'type': 'Demonstration competency',
            'levels': {
                '0': 'Does not communicate effectively about student learning.',
                '1': 'Communicates with limited effectiveness about student learning.',
                '2': 'Uses effective communication with students, parents, and colleagues about student learning.',
                '3': '…and Facilitates collaborative communication to enhance student learning outcomes.'
            }
        },
        {
            'id': 'PR6',
            'code': 'PR6',
            'title': 'Collaborate effectively with colleagues to support student learning and professional growth.',
            'context': 'Conference w/MT',
            'competency_area': 'Professional Responsibility',
            'type': 'Application competency',
            'levels': {
                '0': 'Does not collaborate with colleagues or works in isolation.',
                '1': 'Shows limited collaboration with colleagues.',
                '2': 'Collaborates effectively with colleagues to support student learning and professional growth.',
                '3': '…and Takes leadership in collaborative efforts to improve school culture and student outcomes.'
            }
        },
        {
            'id': 'PR7',
            'code': 'PR7',
            'title': 'Secure student data and respect confidentiality related to student data.',
            'context': 'Conference w/MT',
            'competency_area': 'Professional Responsibility',
            'type': 'Demonstration competency',
            'levels': {
                '0': 'Does not secure student data or respect confidentiality.',
                '1': 'Shows limited understanding of data security and confidentiality.',
                '2': 'Secures student data and respects confidentiality appropriately.',
                '3': '…and Advocates for proper data security practices with colleagues.'
            }
        }
    ]

def get_evaluator_role_for_item(item):
    """Determine evaluator role based on item context and official STER assignments"""
    item_code = item.get('code', '')
    
    # Supervisor items (19 total): LL2-LL7, IC1/IC2, IC3, IC4, IC5/IC6, IC7, IP1-IP8
    supervisor_codes = [
        # Learners and Learning (6 items)
        'LL2', 'LL3', 'LL4', 'LL5', 'LL6', 'LL7',
        # Instructional Clarity (5 items) 
        'IC1/IC2', 'IC3', 'IC4', 'IC5/IC6', 'IC7',
        # Instructional Practice (8 items)
        'IP1', 'IP2', 'IP3', 'IP4', 'IP5', 'IP6', 'IP7', 'IP8'
    ]
    
    # Cooperating Teacher items (16 total): LL1, CC1-CC8, PR1-PR7
    cooperating_teacher_codes = [
        # Learners and Learning (1 item)
        'LL1',
        # Classroom Climate (8 items)
        'CC1', 'CC2', 'CC3', 'CC4', 'CC5', 'CC6', 'CC7', 'CC8',
        # Professional Responsibility (7 items)
        'PR1', 'PR2', 'PR3', 'PR4', 'PR5', 'PR6', 'PR7'
    ]
    
    if item_code in supervisor_codes:
        return 'supervisor'
    elif item_code in cooperating_teacher_codes:
        return 'cooperating_teacher'
    else:
        # Fallback for field evaluation items or unknown items
        context = item.get('context', '')
        if 'Conference w/MT' in context and 'Observation' not in context:
            return 'cooperating_teacher'
        else:
            return 'supervisor'

def filter_items_by_evaluator_role(items, evaluator_role):
    """Filter STER items based on evaluator role (supervisor vs cooperating_teacher)"""
    filtered_items = []
    
    for item in items:
        item_role = get_evaluator_role_for_item(item)
        
        # Include item if it matches the evaluator role
        if item_role == evaluator_role:
            filtered_items.append(item)
    
    return filtered_items

def get_professional_dispositions():
    """Get professional dispositions for evaluation - Only dispositions 2 and 6"""
    return [
        {
            'id': 'high_learning_expectations',
            'name': 'High Learning Expectations for Each Student',
            'description': 'Views each student through an asset-based lens and believes they can achieve rigorous academic standards and social and emotional competence.',
            'criteria': [
                'Prepares and enacts instruction that demonstrates positive verbal and non-verbal affect',
                'Uses data and data analysis to inform future instruction to alter lessons as necessary to meet individual students\' needs',
                'Routinely gathers instructional materials from multiple sources and seeks additional content knowledge when necessary to ensure learning objectives are met',
                'Utilizes effective instructional techniques that include and engage all learners',
                'Aligns educational technology with instructional goals to enhance student learning'
            ]
        },
        {
            'id': 'educational_equity',
            'name': 'Educational Equity',
            'description': 'Demonstrates educational equity by developing and maintaining an inclusive learning environment that values individual, family, and community assets.',
            'criteria': [
                'Leverages personal or social identities such as gender, disability, ethnic origins, sexual orientation, race, immigration status, native language, or family background as assets that enhance the classroom learning environment',
                'Welcomes and respects cultural and academic diversity, considers issues in terms of multiple perspectives, and demonstrates leadership by modeling culturally inclusive beliefs and behaviors',
                'Considers difference in student backgrounds, interests, and attitudes while incorporating culturally inclusive perspectives in all instructional planning',
                'Implements equitable and appropriate learning experiences for all students, including those with disabilities and language learners',
                'Develops and maintains an inclusive classroom where all students experience a sense of belonging and support'
            ]
        }
    ] 