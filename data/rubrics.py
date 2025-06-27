"""
Rubric data for AI-STER evaluation system
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
        {
            'id': 'LL1',
            'code': 'LL1',
            'title': 'Participate in meetings with student\'s parents/guardians (e.g., IEP, 504, behavior, attendance, parent teacher conferences) to help assess and plan needed student support.',
            'context': 'Conference w/MT',
            'competency_area': 'Learners and Learning',
            'type': 'Demonstration competency',
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
        {
            'id': 'IC1_IC2_STER',
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
            },
            'example_justification': 'The student teacher demonstrates a thorough understanding of the Utah Core Standards and consistently aligns learning intentions and success criteria with these standards. By aligning learning intentions and success criteria with the Utah Core Standards, the student teacher provides students with a clear understanding of expectations and purpose.'
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
            'id': 'A1',
            'code': 'A1',
            'title': 'Use multiple assessment strategies to monitor student learning.',
            'context': 'Observation or Conference w/MT and ST',
            'competency_area': 'Assessment',
            'type': 'Application competency',
            'levels': {
                '0': 'Does not use assessment strategies to monitor student learning.',
                '1': 'Uses limited assessment strategies to monitor student learning.',
                '2': 'Uses multiple assessment strategies to monitor student learning.',
                '3': '…and Uses assessment data to differentiate instruction for individual students.'
            }
        },
        {
            'id': 'A2',
            'code': 'A2',
            'title': 'Analyze assessment data to inform instructional decisions.',
            'context': 'Observation or Conference w/MT and ST',
            'competency_area': 'Assessment',
            'type': 'Application competency',
            'levels': {
                '0': 'Does not analyze assessment data.',
                '1': 'Collects assessment data but does not analyze it to inform instruction.',
                '2': 'Analyzes assessment data to inform instructional decisions.',
                '3': '…and Uses data analysis to modify instruction in real-time based on student needs.'
            }
        }
    ]

def get_professional_dispositions():
    """Get professional dispositions for evaluation"""
    return [
        {
            'id': 'self_efficacy',
            'name': 'Self-Efficacy',
            'description': 'Recognizes that intelligence, talents, and abilities can be developed through intentional effort, persistence, and input from others.',
            'criteria': [
                'Recognizes personal strengths and uses them to professional advantage',
                'Recognizes limitations, is willing to change, and works to develop solutions on own before asking for support',
                'Shows intellectual curiosity and demonstrates professional initiative by creating learning opportunities for self',
                'Reflects on and models professional growth for others',
                'Understands that productive struggle is part of the learning process and demonstrates resilience'
            ]
        },
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
            'id': 'ethical_professional',
            'name': 'Ethical/Professional',
            'description': 'Values professional conduct and ethics and respects students, families, communities, and colleagues.',
            'criteria': [
                'Demonstrates an understanding and follows appropriate education laws, ethics, and standards; follows program and university policies',
                'Demonstrates professionalism by exhibiting punctual attendance, completing tasks on time, and responding promptly and professionally in all communications',
                'Establishes and maintains appropriate relationships with peers, faculty, staff, and others (including students)',
                'Productively collaborates in academic and professional settings and keeps personal and professional confidences with colleagues'
            ]
        },
        {
            'id': 'reflective_practitioner',
            'name': 'Reflective Practitioner',
            'description': 'Values a personal commitment to continuous growth and professional learning by fostering self-reflection and acting on feedback.',
            'criteria': [
                'Actively seeks and is willing to apply supportive and corrective feedback from others to make positive change',
                'Receptive to new ideas and techniques',
                'Critically analyzes and reflects on own learning and teaching and makes changes',
                'Uses critical reflection to seek out, analyze, and apply current research to improve teaching practice'
            ]
        },
        {
            'id': 'emotionally_intelligent',
            'name': 'Emotionally Intelligent',
            'description': 'Exhibits awareness, control, and expression of one\'s emotions in multiple contexts to navigate interpersonal relationships in academic and professional settings.',
            'criteria': [
                'Demonstrates appropriate professionalism and self-regulation and maintains professional composure',
                'Remains accountable and responsible for own emotions and behaviors',
                'Advocates for the well-being of self and others',
                'Seeks positive outcomes to tough situations through perseverance and appropriate support',
                'Listens actively to the opinions of others and demonstrates respect to others\' viewpoints even when not in agreement',
                'Demonstrates empathy, compassion, and social awareness'
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