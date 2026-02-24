"""
init_db.py
Run once to create the database and seed sample questions.
Usage: python init_db.py
"""

import sqlite3

DATABASE = "nuclear_quiz.db"

def init_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")

    with open("schema.sql") as f:
        db.executescript(f.read())

    db.commit()
    print("Database initialized and categories seeded.")
    seed_sample_questions(db)
    db.commit()
    print("Sample questions loaded.")
    db.close()


def add_question(db, category_id, question_text, answers, correct_index, explanation, difficulty=1, source=""):
    """
    answers: list of 4 strings
    correct_index: 0-based index of the correct answer
    """
    cursor = db.execute("""
        INSERT INTO questions (category_id, question_text, explanation, difficulty, source)
        VALUES (?, ?, ?, ?, ?)
    """, (category_id, question_text, explanation, difficulty, source))
    question_id = cursor.lastrowid

    for i, answer_text in enumerate(answers):
        db.execute("""
            INSERT INTO answers (question_id, answer_text, is_correct)
            VALUES (?, ?, ?)
        """, (question_id, answer_text, 1 if i == correct_index else 0))


def seed_sample_questions(db):

    # ── CANDU REACTOR SYSTEMS (category_id = 1) ──────────────────────────

    add_question(db, 1,
        "What is a key feature that distinguishes CANDU reactors from most other power reactor designs?",
        [
            "They use enriched uranium fuel",
            "They are refuelled online at full power",
            "They use light water as both moderator and coolant",
            "They operate at higher core temperatures than PWRs"
        ],
        correct_index=1,
        explanation="CANDU reactors use horizontal fuel channels that allow refuelling while the reactor is at full power, eliminating the need for planned outages for refuelling. They also use natural uranium fuel and heavy water as both moderator and coolant.",
        difficulty=1,
        source="IAEA-TECDOC-1391"
    )

    add_question(db, 1,
        "In a CANDU reactor, what is the function of the calandria?",
        [
            "It houses the steam generators",
            "It is the low-pressure vessel containing the heavy water moderator",
            "It is the high-pressure vessel containing the coolant",
            "It houses the reactor control computers"
        ],
        correct_index=1,
        explanation="The calandria is a horizontal cylindrical vessel that contains the heavy water moderator at low temperature and pressure. The pressure tubes (containing fuel and high-pressure coolant) pass through the calandria tubes inside it.",
        difficulty=1,
        source="IAEA-TECDOC-1391"
    )

    add_question(db, 1,
        "CANDU reactors have two independent fast shutdown systems. What is the primary shutdown mechanism of SDS1?",
        [
            "Injection of gadolinium nitrate into the moderator",
            "Dropping of mechanical control absorbers into the core",
            "Draining of the heavy water moderator",
            "Insertion of boron rods into fuel channels"
        ],
        correct_index=1,
        explanation="Shutdown System 1 (SDS1) uses shutoff rods — 28 mechanical absorbers that drop by gravity into the reactor core. SDS2 injects high-pressure gadolinium nitrate poison into the moderator. The two systems are fully independent to meet defence-in-depth requirements.",
        difficulty=2,
        source="CNSC REGDOC-2.4.1"
    )

    add_question(db, 1,
        "What moderator material is used in CANDU reactors and why?",
        [
            "Graphite, because it is cheap and widely available",
            "Light water, because it is effective at thermalizing neutrons",
            "Heavy water (D₂O), because it absorbs fewer neutrons than light water",
            "Beryllium, because it has a very small neutron absorption cross-section"
        ],
        correct_index=2,
        explanation="Heavy water (deuterium oxide, D₂O) has a much lower neutron absorption cross-section than light water. This allows CANDU reactors to use natural uranium fuel (0.7% U-235) rather than enriched uranium, because fewer neutrons are lost to the moderator.",
        difficulty=2,
        source="IAEA Nuclear Power Reactor Characteristics"
    )

    add_question(db, 1,
        "What does LOCA stand for and why is it a key design basis event for CANDU reactors?",
        [
            "Loss of Coolant Accident — a break in the primary heat transport system that can uncover fuel",
            "Loss of Control Accident — failure of reactor regulation systems",
            "Loss of Cooling Accident — failure of the secondary coolant loop",
            "Large Output Control Anomaly — unexpected power excursion"
        ],
        correct_index=0,
        explanation="A Loss of Coolant Accident (LOCA) involves a break in the Primary Heat Transport (PHT) system. If coolant is lost, fuel could overheat. CANDU's Emergency Core Cooling System (ECCS) is designed to inject water into fuel channels to prevent fuel damage following a LOCA.",
        difficulty=2,
        source="CNSC REGDOC-2.4.2"
    )

    # ── CNSC REGULATORY FRAMEWORK (category_id = 2) ──────────────────────

    add_question(db, 2,
        "Under the Nuclear Safety and Control Act, which document sets out the conditions under which a nuclear facility may operate?",
        [
            "Safety Analysis Report",
            "Licence Conditions Handbook (LCH)",
            "Nuclear Security Regulations",
            "CNSC Staff Assessment Report"
        ],
        correct_index=1,
        explanation="The Licence Conditions Handbook (LCH) is the primary document that defines the specific conditions attached to a nuclear facility's operating licence. It translates regulatory requirements into facility-specific obligations.",
        difficulty=1,
        source="NSCA, S.C. 1997, c. 9"
    )

    add_question(db, 2,
        "What does the CNSC REGDOC series number 2.4 relate to?",
        [
            "Security of nuclear substances",
            "Safety analysis",
            "Radiation protection",
            "Human performance management"
        ],
        correct_index=1,
        explanation="CNSC REGDOCs are organized by safety and control area. The 2.x series covers Safety Analysis, with 2.4 specifically addressing deterministic safety analysis and 2.6 covering emergency core cooling.",
        difficulty=2,
        source="CNSC Regulatory Framework"
    )

    add_question(db, 2,
        "What is the primary purpose of a CNSC Compliance Verification Commission (CVC) hearing?",
        [
            "To approve new reactor designs",
            "To review licensee performance and renew or amend operating licences",
            "To investigate nuclear accidents",
            "To set annual radiation dose limits for workers"
        ],
        correct_index=1,
        explanation="The CNSC Commission holds public hearings to review licensee compliance performance and to make decisions on licence renewals or amendments. These proceedings are quasi-judicial and allow public participation.",
        difficulty=2,
        source="NSCA Section 22"
    )

    # ── IAEA SAFETY STANDARDS (category_id = 3) ──────────────────────────

    add_question(db, 3,
        "What are the three levels of the IAEA Safety Standards Series, from highest to lowest authority?",
        [
            "Safety Guides, Safety Reports, Safety Fundamentals",
            "Safety Fundamentals, Safety Requirements, Safety Guides",
            "General Safety Guides, Specific Safety Guides, Technical Documents",
            "Safety Requirements, Safety Fundamentals, Safety Reports"
        ],
        correct_index=1,
        explanation="The IAEA Safety Standards have three levels: Safety Fundamentals (SF) state the fundamental safety objective and principles; Safety Requirements (GSR/SSR) state what must be done; Safety Guides (GSG/SSG) provide recommendations on how to meet requirements.",
        difficulty=1,
        source="IAEA SF-1"
    )

    add_question(db, 3,
        "According to IAEA SF-1, what is the fundamental safety objective?",
        [
            "To minimize the cost of nuclear energy production",
            "To protect people and the environment from harmful effects of ionizing radiation",
            "To maximize the availability of nuclear power plants",
            "To ensure nuclear material is not diverted for weapons purposes"
        ],
        correct_index=1,
        explanation="IAEA Safety Fundamentals document SF-1 states that the fundamental safety objective is to protect people and the environment from harmful effects of ionizing radiation. All safety measures must be directed at achieving this objective.",
        difficulty=1,
        source="IAEA SF-1, para 1.1"
    )

    add_question(db, 3,
        "How many levels of defence in depth are defined in IAEA safety standards for nuclear power plants?",
        [
            "Three",
            "Four",
            "Five",
            "Six"
        ],
        correct_index=2,
        explanation="IAEA defines five levels of defence in depth: (1) prevention of abnormal operation and failures, (2) control of abnormal operation, (3) control of accidents within design basis, (4) control of severe plant conditions, and (5) mitigation of radiological consequences of significant releases.",
        difficulty=2,
        source="IAEA SSR-2/1 Rev.1"
    )

    # ── RADIATION PROTECTION (category_id = 4) ──────────────────────────

    add_question(db, 4,
        "What does ALARA stand for and what is its significance in radiation protection?",
        [
            "As Low As Reasonably Achievable — doses should be reduced beyond regulatory limits where practical",
            "Allowable Limits for Active Radiation Areas — defines zone boundaries in nuclear plants",
            "Annual Limit for Allowable Radiation in Atmosphere — environmental discharge standard",
            "As Low As Reliably Achievable — minimum detectable dose for dosimetry equipment"
        ],
        correct_index=0,
        explanation="ALARA (As Low As Reasonably Achievable) is a core radiation protection principle requiring that radiation doses be kept as low as reasonably achievable, taking economic and social factors into account. It goes beyond simply meeting dose limits.",
        difficulty=1,
        source="IAEA GSR Part 3; CNSC REGDOC-2.7.1"
    )

    add_question(db, 4,
        "Under CNSC regulations, what is the effective dose limit for nuclear energy workers over a five-year dosimetry period?",
        [
            "20 mSv/year (100 mSv over 5 years)",
            "50 mSv/year (250 mSv over 5 years)",
            "100 mSv over 5 years with no more than 50 mSv in a single year",
            "20 mSv in any single year with no five-year limit"
        ],
        correct_index=2,
        explanation="The Radiation Protection Regulations set an effective dose limit of 100 mSv over any 5-year dosimetry period, with no more than 50 mSv in a single year for nuclear energy workers. This aligns with ICRP Publication 103 recommendations.",
        difficulty=2,
        source="Radiation Protection Regulations, SOR/2000-203"
    )

    # ── NUCLEAR SECURITY & SAFEGUARDS (category_id = 5) ──────────────────

    add_question(db, 5,
        "What is the purpose of IAEA safeguards?",
        [
            "To protect nuclear facilities from physical attack",
            "To verify that nuclear material is not diverted from peaceful use to weapons purposes",
            "To ensure nuclear waste is managed safely",
            "To regulate the international trade of nuclear equipment"
        ],
        correct_index=1,
        explanation="IAEA safeguards are a system of verification measures that provide credible assurance that States are honoring their obligations not to divert nuclear material from peaceful uses to nuclear weapons. They are based on nuclear material accountancy supplemented by containment and surveillance.",
        difficulty=1,
        source="IAEA INFCIRC/153"
    )

    add_question(db, 5,
        "What is the document that forms the basis for a State's Comprehensive Safeguards Agreement with the IAEA?",
        [
            "INFCIRC/225",
            "INFCIRC/153",
            "INFCIRC/66",
            "INFCIRC/540"
        ],
        correct_index=1,
        explanation="INFCIRC/153 ('The Structure and Content of Agreements between the Agency and States Required in Connection with the Treaty on the Non-Proliferation of Nuclear Weapons') is the model for Comprehensive Safeguards Agreements (CSAs) required of all NPT non-nuclear-weapon states.",
        difficulty=3,
        source="IAEA INFCIRC/153"
    )

    add_question(db, 5,
        "What does an Additional Protocol (AP) to a safeguards agreement require a State to provide?",
        [
            "Physical protection measures for nuclear facilities",
            "Expanded declarations and broader access for IAEA inspectors beyond nuclear material",
            "Elimination of all existing nuclear weapons",
            "Export controls on nuclear-related equipment"
        ],
        correct_index=1,
        explanation="The Additional Protocol (model in INFCIRC/540) significantly strengthens safeguards by requiring states to declare a broader range of nuclear-related activities (including R&D, fuel cycle activities, imports/exports) and granting the IAEA broader inspection access rights.",
        difficulty=2,
        source="IAEA INFCIRC/540"
    )

    print(f"Seeded sample questions across 5 categories.")


if __name__ == "__main__":
    init_db()
