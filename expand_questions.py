"""
expand_questions.py
Expands existing categories to 20 questions each, and adds three new categories:
  - PWR Reactor Systems (international)
  - BWR Reactor Systems (international)
  - INPO and WANO

Usage: python expand_questions.py
"""

import sqlite3
import os

DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nuclear_quiz.db")


def add_question(db, category_id, question_text, answers, correct_index, explanation, difficulty=1, source=""):
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


def add_category(db, name, description, icon):
    cursor = db.execute(
        "INSERT INTO categories (name, description, icon) VALUES (?, ?, ?)",
        (name, description, icon)
    )
    return cursor.lastrowid


def main():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")

    # ═══════════════════════════════════════════════════════════════════════
    # TOP UP EXISTING CATEGORIES TO 20 QUESTIONS EACH
    # ═══════════════════════════════════════════════════════════════════════

    # ── CANDU REACTOR SYSTEMS — add 7 more to reach 20 (cat id = 1) ────────

    add_question(db, 1,
        "What is the primary heat transport (PHT) system pressure and temperature at normal CANDU reactor operating conditions?",
        [
            "Approximately 10 MPa and 250°C",
            "Approximately 10 MPa and 310°C at the reactor outlet",
            "Approximately 16 MPa and 325°C, the same as a typical PWR",
            "Approximately 7 MPa and 285°C"
        ],
        correct_index=1,
        explanation="The CANDU PHT system operates at approximately 10 MPa (1450 psi) with coolant temperatures of about 265°C at the inlet and 310°C at the reactor outlet headers. This is lower than a typical PWR (~15.5 MPa) because the pressure tubes rather than a single large pressure vessel contain the high-pressure coolant.",
        difficulty=2,
        source="IAEA-TECDOC-1391"
    )

    add_question(db, 1,
        "What is the function of the liquid zone controllers (LZCs) in a CANDU reactor?",
        [
            "They provide emergency poison injection capability as part of SDS2",
            "They are water-filled compartments in the core used for fine reactivity control and flux shaping",
            "They regulate the flow of heavy water coolant through the fuel channels",
            "They control the temperature of the heavy water moderator"
        ],
        correct_index=1,
        explanation="Liquid zone controllers are 14 compartments distributed throughout the CANDU core, each partially filled with light water. By varying the light water level (which absorbs neutrons), the reactor control system performs fine adjustments to reactor power and three-dimensional flux shaping during normal operations.",
        difficulty=2,
        source="IAEA-TECDOC-1391"
    )

    add_question(db, 1,
        "Why does a CANDU reactor have a relatively long neutron prompt lifetime compared to light water reactors?",
        [
            "Because the fuel enrichment is lower, requiring more fissions per unit time",
            "Because heavy water moderator absorbs fewer neutrons, resulting in a larger thermal neutron population and longer diffusion time",
            "Because the large core volume means neutrons travel farther before causing fission",
            "Because the online refuelling process continuously introduces fresh fuel"
        ],
        correct_index=1,
        explanation="Heavy water has a much lower neutron absorption cross-section than light water, resulting in fewer neutron absorptions per unit path length. This means neutrons diffuse further and live longer in the CANDU moderator before causing fission. The longer prompt neutron lifetime (around 1 ms vs ~0.1 ms for LWRs) gives operators slightly more time to respond to power transients.",
        difficulty=3,
        source="IAEA Nuclear Reactor Theory"
    )

    add_question(db, 1,
        "What is the significance of tritium in CANDU reactor operations?",
        [
            "Tritium is produced in the heavy water moderator and coolant through neutron activation of deuterium, requiring management as a radioactive byproduct",
            "Tritium is added to the coolant as a neutron poison during startup",
            "Tritium is a fission product that must be monitored in spent fuel storage",
            "Tritium is used as a burnable absorber in CANDU fuel bundles"
        ],
        correct_index=0,
        explanation="Deuterium in the heavy water absorbs neutrons to produce tritium (H-3), a radioactive isotope with a 12.3-year half-life that emits beta radiation. Managing tritium in the moderator and coolant systems — including controlling worker dose from tritium ingestion and inhalation — is a significant operational consideration unique to heavy water reactors.",
        difficulty=2,
        source="CNSC REGDOC-2.7.1"
    )

    add_question(db, 1,
        "What is a CANDU fuel bundle and how many fuel pellets does a standard 37-element bundle contain?",
        [
            "A cluster of 19 fuel rods containing approximately 285 UO₂ pellets",
            "A cluster of 37 fuel rods containing approximately 480 UO₂ pellets",
            "A single fuel rod assembly containing 37 fuel pellets",
            "A square 6×6 array of fuel pins containing 324 UO₂ pellets"
        ],
        correct_index=1,
        explanation="A standard CANDU 37-element fuel bundle consists of 37 fuel rods (elements) arranged in concentric rings around a central rod, all held together by end plates. Each rod contains approximately 13 UO₂ pellets, giving about 480 pellets per bundle. Each fuel channel contains 12 bundles. The compact bundle design allows online refuelling.",
        difficulty=2,
        source="IAEA-TECDOC-1391"
    )

    add_question(db, 1,
        "What is the purpose of the reactor building (containment) in a CANDU nuclear plant?",
        [
            "To house the control room and reactor operations staff",
            "To act as the final barrier preventing release of radioactive material to the environment in accident conditions",
            "To provide shielding for the steam generators and turbine hall",
            "To house the spent fuel storage bay and waste management systems"
        ],
        correct_index=1,
        explanation="The CANDU reactor building is a pre-stressed concrete containment structure that forms the final physical barrier against the release of radioactive material to the environment. It is designed to remain intact and leak-tight following design basis accidents including a large LOCA. It also houses the reactor core, PHT system, and associated safety systems.",
        difficulty=1,
        source="CNSC REGDOC-2.4.1"
    )

    add_question(db, 1,
        "What is the dousing system in a CANDU reactor building and when does it actuate?",
        [
            "A fire suppression system in the turbine hall",
            "A water spray system in the reactor vault that cools moderator equipment",
            "A large water tank and spray system that suppresses pressure and temperature inside the reactor building following a LOCA",
            "A decontamination spray system used during planned maintenance outages"
        ],
        correct_index=2,
        explanation="The CANDU reactor building dousing system consists of a large water tank (typically ~1400 m³) at the top of the containment dome connected to spray nozzles. Following a LOCA, steam released into the reactor building is condensed by the dousing spray, limiting pressure buildup and maintaining containment integrity.",
        difficulty=2,
        source="CNSC REGDOC-2.4.1"
    )

    # ── CNSC REGULATORY FRAMEWORK — add 10 more to reach 20 (cat id = 2) ───

    add_question(db, 2,
        "What is the role of CNSC's Designated Officer (DO) in the licensing process?",
        [
            "A senior CNSC staff member authorized to make certain licensing decisions without a full Commission hearing",
            "An independent safety inspector assigned to each nuclear power plant",
            "A government-appointed official who approves all major nuclear projects",
            "A technical reviewer who assesses licence applications before Commission hearings"
        ],
        correct_index=0,
        explanation="A Designated Officer is a senior CNSC staff member delegated authority by the Commission to make certain regulatory decisions — such as issuing, amending, or revoking licences for lower-risk activities — without requiring a full public Commission hearing. This allows the CNSC to process routine licensing matters efficiently.",
        difficulty=2,
        source="Nuclear Safety and Control Act, Section 37"
    )

    add_question(db, 2,
        "What is the purpose of the CNSC's Integrated Improvement Plan (IIP)?",
        [
            "A plan developed by the CNSC to improve its own internal regulatory processes",
            "A licensee-developed plan to address areas of low performance identified during CNSC regulatory oversight",
            "An annual plan submitted by nuclear operators forecasting planned maintenance outages",
            "A CNSC program for improving public communication about nuclear safety"
        ],
        correct_index=1,
        explanation="When CNSC regulatory oversight identifies areas where a licensee's performance is below expectations, the licensee may be required to develop an Integrated Improvement Plan (IIP) outlining specific corrective actions, timelines, and success metrics. The CNSC tracks IIP progress as part of ongoing compliance verification.",
        difficulty=2,
        source="CNSC Regulatory Framework"
    )

    add_question(db, 2,
        "What does the CNSC's 'compliance continuum' concept describe?",
        [
            "A scale from full compliance to criminal prosecution used to categorize licensee violations",
            "A range of regulatory tools from promotion and verification through to enforcement actions that the CNSC applies based on risk and performance",
            "The spectrum of radiation doses from background levels to occupational limits",
            "A timeline from licence application through to decommissioning"
        ],
        correct_index=1,
        explanation="The CNSC compliance continuum describes a range of regulatory tools used based on a licensee's performance and the risk significance of findings. At one end are promotion and education activities; moving through compliance verification, then graduated enforcement actions (orders, licence amendments, monetary penalties), and at the far end, licence revocation or prosecution.",
        difficulty=2,
        source="CNSC Regulatory Framework"
    )

    add_question(db, 2,
        "Under the Nuclear Security Regulations, what is a 'protected area' at a Canadian nuclear facility?",
        [
            "The area within the plant boundary where the public is not permitted",
            "An area within the outer perimeter where nuclear material is processed or stored and additional security measures apply",
            "The exclusion zone surrounding the plant within which emergency planning is required",
            "A classified area where sensitive nuclear information is stored"
        ],
        correct_index=1,
        explanation="Under the Nuclear Security Regulations, a protected area is a defined area within a nuclear facility where nuclear material is processed, used, or stored. It requires physical barriers, access control, and security monitoring beyond those at the facility perimeter. Higher-security 'inner areas' may exist within the protected area for the most sensitive material.",
        difficulty=2,
        source="Nuclear Security Regulations, SOR/2000-209"
    )

    add_question(db, 2,
        "What environmental assessment process applied to major new nuclear facilities in Canada prior to the Impact Assessment Act (2019)?",
        [
            "Canadian Environmental Assessment Act (CEAA 2012)",
            "Nuclear Environmental Assessment Regulations",
            "CNSC Environmental Review Process",
            "National Energy Board Environmental Assessment"
        ],
        correct_index=0,
        explanation="Major nuclear projects in Canada were subject to the Canadian Environmental Assessment Act (CEAA 2012) for federal environmental assessments, often conducted jointly with the CNSC licensing process. In 2019 CEAA 2012 was replaced by the Impact Assessment Act (IAA), which established a new federal impact assessment process applicable to designated nuclear projects.",
        difficulty=3,
        source="Impact Assessment Act, S.C. 2019, c. 28"
    )

    add_question(db, 2,
        "What is the significance of CNSC's REGDOC-3.1.1 regarding reporting requirements?",
        [
            "It sets out financial reporting requirements for nuclear licensees",
            "It establishes requirements for reporting of nuclear incidents, events, and other information to the CNSC",
            "It requires annual safety performance reports to be submitted to the Commission",
            "It governs reporting of nuclear material exports to foreign countries"
        ],
        correct_index=1,
        explanation="CNSC REGDOC-3.1.1 sets out requirements for licensees to report nuclear events, incidents, and other safety-relevant information to the CNSC. It defines reporting timelines (immediate, 24-hour, and routine) based on event significance and type, ensuring the CNSC receives timely information to assess safety implications.",
        difficulty=2,
        source="CNSC REGDOC-3.1.1"
    )

    add_question(db, 2,
        "What is the purpose of the CNSC's periodic safety review (PSR) requirement for nuclear power plants?",
        [
            "An annual safety inspection conducted by CNSC inspectors at each nuclear plant",
            "A comprehensive assessment conducted approximately every 10 years to confirm a plant's continued safe operation and identify improvements",
            "A safety review required before each refuelling outage",
            "A post-accident review triggered by any significant event at a Canadian nuclear plant"
        ],
        correct_index=1,
        explanation="A Periodic Safety Review (PSR) is a comprehensive, systematic assessment of a nuclear power plant conducted approximately every 10 years (or at major licence renewal). It evaluates the plant against current safety standards, assesses aging, and identifies any gaps requiring corrective action. The PSR informs licence renewal decisions and long-term operation approvals.",
        difficulty=2,
        source="CNSC REGDOC-2.3.3"
    )

    add_question(db, 2,
        "What does the term 'defence in depth' mean within the CNSC regulatory context?",
        [
            "Regulatory oversight applied at multiple levels: federal, provincial, and municipal",
            "Multiple independent physical barriers and safety systems so no single failure results in radiological harm",
            "The depth of regulatory scrutiny applied proportional to the risk of each licensed activity",
            "The number of layers of regulatory approval required for major nuclear projects"
        ],
        correct_index=1,
        explanation="Within CNSC's regulatory framework, defence in depth requires multiple independent physical barriers (fuel matrix, fuel sheath, pressure boundary, containment) and safety systems (process systems, safety systems, mitigation measures) such that no single failure leads to radiological harm. CNSC verifies licensees maintain this defence in depth through design and operations.",
        difficulty=1,
        source="CNSC REGDOC-2.4.1"
    )

    add_question(db, 2,
        "What is the Canadian requirement for nuclear liability under the Nuclear Liability and Compensation Act?",
        [
            "Nuclear operators are not required to carry liability insurance as the government self-insures",
            "Operators must carry $1 billion CAD in nuclear liability insurance with absolute liability regardless of fault",
            "Operators must carry $650 million CAD in coverage under a pooled insurance arrangement",
            "There is no specified minimum — coverage is determined by each province"
        ],
        correct_index=1,
        explanation="Canada's Nuclear Liability and Compensation Act (in force 2017) establishes absolute liability — operators are liable regardless of fault — with a minimum liability limit of $1 billion CAD. This aligns Canada with international conventions (Paris Convention, Vienna Convention) on nuclear liability and provides compensation to the public in the event of a nuclear incident.",
        difficulty=3,
        source="Nuclear Liability and Compensation Act, S.C. 2015, c. 4"
    )

    add_question(db, 2,
        "What is the role of the Canadian Nuclear Safety Commission in relation to provincial regulators?",
        [
            "The CNSC is subordinate to provincial regulators for routine nuclear plant operations",
            "The CNSC is the sole federal regulator for nuclear safety in Canada; provinces have no jurisdiction over nuclear matters under the Constitution",
            "Provincial regulators and the CNSC share jurisdiction over nuclear power plants",
            "The CNSC only regulates uranium mining; provinces regulate all other nuclear activities"
        ],
        correct_index=1,
        explanation="Under the Constitution Act, nuclear energy is a federal matter in Canada. The CNSC, established under the Nuclear Safety and Control Act, has exclusive federal jurisdiction over nuclear safety regulation. Provincial regulators (such as provincial utilities commissions) may have jurisdiction over economic matters, but nuclear safety is solely the CNSC's domain.",
        difficulty=2,
        source="Constitution Act, 1867; Nuclear Safety and Control Act"
    )

    # ── IAEA SAFETY STANDARDS — add 11 more to reach 20 (cat id = 3) ────────

    add_question(db, 3,
        "What is the IAEA's Convention on Early Notification of a Nuclear Accident?",
        [
            "A treaty requiring states to notify the IAEA within 24 hours of any nuclear power plant trip",
            "A legally binding convention requiring states to notify the IAEA and potentially affected states of nuclear accidents that could cause transboundary radiological consequences",
            "An IAEA resolution recommending voluntary notification of nuclear incidents among member states",
            "A bilateral agreement between neighboring states with nuclear facilities"
        ],
        correct_index=1,
        explanation="The Convention on Early Notification of a Nuclear Accident (INFCIRC/335), in force since 1986 and prompted by Chernobyl, requires signatory states to notify the IAEA and potentially affected states immediately following a nuclear accident that could cause transboundary releases. The IAEA then acts as a communication hub to share information with all member states.",
        difficulty=2,
        source="IAEA INFCIRC/335"
    )

    add_question(db, 3,
        "What is the IAEA's International Nuclear and Radiological Event Scale (INES)?",
        [
            "A 7-level scale for communicating the safety significance of nuclear and radiological events to the public",
            "An internal IAEA classification system for prioritizing safety inspection missions",
            "A legal framework for categorizing nuclear accidents for liability purposes",
            "A grading system for the quality of national nuclear regulatory frameworks"
        ],
        correct_index=0,
        explanation="INES is a 7-level logarithmic scale used to communicate the safety significance of nuclear and radiological events to the public. Levels 1-3 are 'incidents', levels 4-7 are 'accidents'. Level 7 (major accident) has been assigned to Chernobyl and Fukushima; Level 5 to Three Mile Island. Below Level 1 are 'deviations' with no safety significance.",
        difficulty=1,
        source="IAEA INES User's Manual"
    )

    add_question(db, 3,
        "What is the purpose of the IAEA's Generic Reactor Safety Review (GRSR) service?",
        [
            "A mandatory review of all new reactor designs before they can be licensed in any IAEA member state",
            "A peer review service assessing the safety of a specific reactor design against IAEA safety standards",
            "An annual review of operating nuclear power plant safety performance",
            "A financial review of the economic viability of reactor construction projects"
        ],
        correct_index=1,
        explanation="The IAEA's Generic Reactor Safety Review (GRSR) service provides peer review of a reactor design's safety case against IAEA safety standards at the request of the vendor or state. It is not a licensing approval — national regulators retain licensing authority — but provides an independent international assessment that can support national licensing processes.",
        difficulty=3,
        source="IAEA Safety Standards"
    )

    add_question(db, 3,
        "According to IAEA SSR-2/1, what are the key siting considerations for a nuclear power plant?",
        [
            "Proximity to large population centers, grid connection capacity, and cooling water availability only",
            "External hazards, population distribution, emergency planning feasibility, and environmental impact",
            "Land cost, labor availability, and transmission infrastructure",
            "Seismic zone classification and distance from national borders"
        ],
        correct_index=1,
        explanation="IAEA SSR-2/1 requires siting assessments to evaluate: external hazards (seismic, flooding, extreme weather, industrial/transport hazards), population distribution around the site, feasibility of emergency planning, and environmental impacts. The site must be suitable for the plant design's safety case and emergency response requirements.",
        difficulty=2,
        source="IAEA SSR-2/1 Rev.1"
    )

    add_question(db, 3,
        "What is the IAEA's Systematic Approach to Training (SAT) and why is it significant for nuclear power plants?",
        [
            "A financial framework for budgeting nuclear operator training programs",
            "A five-phase methodology (Analysis, Design, Development, Implementation, Evaluation) ensuring training is job-relevant and competency-based",
            "A mandatory IAEA certification program for nuclear power plant operators",
            "An international standard for nuclear engineering university curricula"
        ],
        correct_index=1,
        explanation="The SAT is a five-phase training methodology: Analysis (identify job tasks and competencies), Design (define learning objectives), Development (create training materials), Implementation (deliver training), and Evaluation (assess effectiveness). The IAEA promotes SAT as the basis for nuclear power plant training programs because it ensures training directly addresses job-required competencies rather than being curriculum-driven.",
        difficulty=2,
        source="IAEA Safety Reports Series No. 25"
    )

    add_question(db, 3,
        "What does IAEA Safety Guide SSG-3 address?",
        [
            "The development and application of level 1 probabilistic safety assessment for nuclear power plants",
            "Radiation protection in the design of nuclear power plants",
            "The management of nuclear fuel cycle facilities",
            "Seismic hazard assessment for nuclear facilities"
        ],
        correct_index=0,
        explanation="IAEA Safety Guide SSG-3 provides guidance on the development and application of Level 1 Probabilistic Safety Assessment (PSA) for nuclear power plants. It covers PSA methodology, scope, quality, and uses in the nuclear safety case. PSA Level 1 assesses the frequency of core damage; Level 2 assesses source terms; Level 3 assesses offsite consequences.",
        difficulty=3,
        source="IAEA SSG-3"
    )

    add_question(db, 3,
        "What is nuclear security culture as defined by the IAEA?",
        [
            "Security policies and physical protection measures at nuclear facilities",
            "The assembly of characteristics, attitudes, and behaviours of individuals, organizations, and institutions that supports and enhances nuclear security",
            "A mandatory training program for security personnel at nuclear power plants",
            "Background screening requirements for nuclear facility employees"
        ],
        correct_index=1,
        explanation="The IAEA defines nuclear security culture as the assembly of characteristics, attitudes, and behaviours in individuals, organizations, and institutions that supports and enhances nuclear security. It parallels the concept of safety culture and recognizes that physical systems alone cannot ensure security without the right human and organizational factors.",
        difficulty=2,
        source="IAEA Nuclear Security Series No. 7"
    )

    add_question(db, 3,
        "What is the difference between 'deterministic safety analysis' and 'probabilistic safety assessment'?",
        [
            "Deterministic analysis is used for new plants; probabilistic assessment is used for older plants",
            "Deterministic analysis evaluates a defined set of postulated events against acceptance criteria; probabilistic assessment quantifies the likelihood and consequences of a wide range of accident sequences",
            "Deterministic analysis covers normal operations; probabilistic assessment covers accident conditions",
            "There is no practical difference — they are complementary names for the same methodology"
        ],
        correct_index=1,
        explanation="Deterministic Safety Analysis (DSA) postulates specific initiating events (design basis accidents) and analyzes them against defined acceptance criteria (e.g., peak fuel temperature limits), without explicitly quantifying probabilities. Probabilistic Safety Assessment (PSA) systematically identifies and quantifies the frequency and consequences of a broad range of accident sequences, providing risk insights. Both are required by CNSC and the IAEA.",
        difficulty=2,
        source="IAEA SSR-2/1; CNSC REGDOC-2.4.2"
    )

    add_question(db, 3,
        "What was the key safety lesson from the Three Mile Island accident (1979) for nuclear power plant operations worldwide?",
        [
            "Reactor containment must be made of reinforced concrete at least 2 metres thick",
            "Operator training, human factors, and control room design are critical safety elements — not just hardware",
            "Pressurized water reactors should be replaced by boiling water reactors",
            "Emergency cooling water systems must be fully automated with no operator control"
        ],
        correct_index=1,
        explanation="The TMI accident revealed that operator training, human factors engineering, control room design, and emergency operating procedures were as important as the physical plant design. Operators misdiagnosed the accident and took actions that worsened the situation. This led to major improvements in simulator training, symptom-based emergency procedures, and human factors throughout the global nuclear industry.",
        difficulty=2,
        source="NUREG-0600; INSAG-1"
    )

    add_question(db, 3,
        "What is the IAEA's role following a nuclear accident in a member state?",
        [
            "The IAEA assumes regulatory control over the affected facility",
            "The IAEA provides technical assistance, coordinates international response, and facilitates information sharing but does not supersede national authority",
            "The IAEA issues binding orders to the affected state's government",
            "The IAEA has no formal role — response is entirely the national government's responsibility"
        ],
        correct_index=1,
        explanation="Following a nuclear accident, the IAEA's role is to support — not replace — national authorities. Under the Convention on Early Notification and the Convention on Assistance, the IAEA coordinates international information sharing, can deploy expert missions (such as Fukushima follow-up missions), and facilitates technical assistance from member states. National regulatory and government authorities retain all decision-making authority.",
        difficulty=2,
        source="IAEA INFCIRC/335; IAEA INFCIRC/336"
    )

    add_question(db, 3,
        "What is the IAEA's PRIS database?",
        [
            "A database of nuclear proliferation incidents and safeguards violations",
            "The Power Reactor Information System — a comprehensive database of nuclear power plant operating data and performance statistics worldwide",
            "A database of IAEA inspection reports and findings",
            "A registry of all radioactive sources in IAEA member states"
        ],
        correct_index=1,
        explanation="PRIS (Power Reactor Information System) is an IAEA database containing comprehensive technical and historical data on nuclear power plants worldwide, including unit capability factors, energy availability factors, unplanned capability loss factors, and lifetime performance data. It is widely used by operators, researchers, and regulators to benchmark performance.",
        difficulty=1,
        source="IAEA PRIS Database"
    )

    # ── RADIATION PROTECTION — add 11 more to reach 20 (cat id = 4) ─────────

    add_question(db, 4,
        "What is the stochastic effect of radiation exposure and how does it differ from a deterministic effect?",
        [
            "Stochastic effects occur immediately following high doses; deterministic effects develop over decades",
            "Stochastic effects (such as cancer) have a probability that increases with dose but no threshold; deterministic effects (such as skin burns) have a threshold below which they do not occur",
            "Stochastic effects affect the whole body; deterministic effects affect only specific organs",
            "Stochastic effects are caused by external radiation; deterministic effects by internal contamination"
        ],
        correct_index=1,
        explanation="Stochastic effects (primarily cancer and hereditary effects) are probabilistic — the chance of occurrence increases with dose but there is no threshold. A single ionizing event could theoretically initiate cancer. Deterministic (tissue reaction) effects occur only above a threshold dose and their severity increases with dose — examples include skin erythema, cataracts, and acute radiation syndrome.",
        difficulty=2,
        source="ICRP Publication 103"
    )

    add_question(db, 4,
        "What is a radiation dose constraint and how does it differ from a dose limit?",
        [
            "A dose constraint is a lower, prospective restriction used in planning and optimization of radiation protection; a dose limit is the regulatory maximum that must never be exceeded",
            "A dose constraint applies to emergency workers; a dose limit applies to routine nuclear workers",
            "A dose constraint is set by the IAEA; a dose limit is set by national regulators",
            "There is no difference — the terms are interchangeable in Canadian regulation"
        ],
        correct_index=0,
        explanation="A dose constraint is a source-related prospective restriction used in optimizing (ALARA) radiation protection for planned exposures — it is below the dose limit and acts as an upper bound for optimization. A dose limit is the regulatory ceiling that must never be exceeded under normal circumstances. Constraints are tools for optimization; limits are regulatory requirements.",
        difficulty=3,
        source="ICRP Publication 103; IAEA GSR Part 3"
    )

    add_question(db, 4,
        "What monitoring is required for workers who may receive internal radiation doses from radioactive contamination?",
        [
            "External personal dosimetry (TLD or OSL badge) is sufficient for all workers",
            "Bioassay programs (urine, fecal, or whole body counting) to detect and quantify internal radionuclide intakes",
            "Continuous air monitoring only — individual worker monitoring is not required",
            "Medical X-ray examination every six months"
        ],
        correct_index=1,
        explanation="Workers who may inhale or ingest radionuclides require internal dosimetry through bioassay programs. Direct methods include whole body counting (for gamma emitters). Indirect methods include urine or fecal bioassay (for alpha and beta emitters like tritium and plutonium). The results are used to calculate committed effective dose from internal intakes.",
        difficulty=2,
        source="CNSC REGDOC-2.7.2; IAEA GSR Part 3"
    )

    add_question(db, 4,
        "What are the four categories of radiation emergency exposure situations according to ICRP?",
        [
            "Minor, significant, severe, and catastrophic",
            "Planned, existing, emergency, and chronic",
            "Occupational, public, medical, and accidental",
            "Planned, existing, and emergency exposure situations (three categories, not four)"
        ],
        correct_index=3,
        explanation="ICRP Publication 103 defines three exposure situations: Planned (deliberate introduction and operation of sources), Existing (already present when decisions are made — natural background, legacy contamination), and Emergency (unexpected situations requiring urgent action). These replace the older concepts of 'practices' and 'interventions' and guide how radiation protection is applied in each context.",
        difficulty=3,
        source="ICRP Publication 103"
    )

    add_question(db, 4,
        "What is the purpose of a Radiation Work Permit (RWP) in nuclear plant operations?",
        [
            "A permit issued by the CNSC authorizing a licensee to perform radiation work",
            "A facility-level document that specifies radiation protection requirements, controls, and dose estimates for a specific task in a radiologically controlled area",
            "A personal certification that a worker has completed radiation safety training",
            "A financial authorization for radiation monitoring equipment purchases"
        ],
        correct_index=1,
        explanation="A Radiation Work Permit (RWP) is an internal plant document — sometimes called a Radiation Protection Work Order — that specifies the radiation conditions expected for a specific task, required protective equipment, dosimetry requirements, dose estimates, and any special controls. Workers must review and acknowledge the RWP before entering radiologically controlled areas for the task.",
        difficulty=1,
        source="CNSC REGDOC-2.7.1"
    )

    add_question(db, 4,
        "What is collective dose and why is it used in radiation protection?",
        [
            "The total dose received by all individuals in an exposed group, measured in person-Sievert, used to estimate the overall population health detriment",
            "The dose received by a worker over their entire career at a nuclear facility",
            "The combined dose from all radionuclides in a worker's body at any given time",
            "The average dose received by all workers at a nuclear power plant in a given year"
        ],
        correct_index=0,
        explanation="Collective dose (person-Sv) is the sum of individual effective doses across all members of an exposed group. It is used to estimate the overall population health detriment from a radiation source or practice, and to compare radiation protection options in optimization (ALARA) analyses. However, ICRP cautions against using collective dose to calculate absolute numbers of predicted health effects.",
        difficulty=2,
        source="ICRP Publication 103; IAEA GSR Part 3"
    )

    add_question(db, 4,
        "What are the main types of personal dosimeters used in nuclear facilities?",
        [
            "Geiger-Müller counters and ionization chambers",
            "Thermoluminescent dosimeters (TLD), optically stimulated luminescence (OSL) dosimeters, and electronic personal dosimeters (EPD)",
            "Scintillation detectors and proportional counters",
            "Film badges and survey meters"
        ],
        correct_index=1,
        explanation="Nuclear workers typically use: TLDs (thermoluminescent dosimeters — crystals that store energy from radiation, released as light when heated for readout), OSL dosimeters (similar principle using light stimulation), and EPDs (electronic personal dosimeters — real-time digital readout with alarm capability). EPDs are increasingly used for real-time dose management; TLD/OSL serve as the official legal dose record.",
        difficulty=1,
        source="CNSC REGDOC-2.7.1"
    )

    add_question(db, 4,
        "What is the significance of radon in the context of radiation protection?",
        [
            "Radon is only a concern for uranium miners and has no relevance to nuclear power plant workers",
            "Radon is a naturally occurring radioactive gas that is the largest contributor to public radiation dose and a significant occupational hazard in uranium mines and some workplaces",
            "Radon is a fission product released during nuclear power plant accidents",
            "Radon is used as a tracer gas to detect leaks in primary heat transport systems"
        ],
        correct_index=1,
        explanation="Radon-222 (from the uranium decay chain) is a naturally occurring radioactive noble gas that accumulates in buildings and underground workplaces. It is the largest single contributor to the average public radiation dose globally. In uranium mines, elevated radon levels create significant occupational exposure requiring careful monitoring and ventilation. Radon lung cancer risk is well established epidemiologically.",
        difficulty=1,
        source="ICRP Publication 115; CNSC REGDOC-2.7.1"
    )

    add_question(db, 4,
        "What is the purpose of contamination control in nuclear facilities?",
        [
            "To prevent radioactive material from spreading beyond controlled areas and causing unintended internal or external doses",
            "To prevent chemical contamination of cooling water systems",
            "To control the spread of industrial chemicals used in plant maintenance",
            "To meet environmental regulations for non-radioactive hazardous materials"
        ],
        correct_index=0,
        explanation="Contamination control prevents the spread of radioactive material — surface contamination or airborne particles — beyond designated controlled areas. This protects workers from internal dose (inhalation/ingestion) and prevents the spread of contamination to non-controlled areas. Key tools include contamination surveys, protective clothing, step-off pads, and contamination-controlled boundaries (change rooms).",
        difficulty=1,
        source="CNSC REGDOC-2.7.1"
    )

    add_question(db, 4,
        "What does 'as low as reasonably achievable' (ALARA) require in practice within a nuclear facility?",
        [
            "Reducing all doses to zero by excluding workers from radiation areas",
            "A documented process of identifying, evaluating, and implementing dose reduction measures taking into account economic and social factors",
            "Ensuring all workers receive exactly the same dose regardless of their role",
            "Applying a fixed percentage reduction to the annual dose limit for each worker"
        ],
        correct_index=1,
        explanation="ALARA in practice requires licensees to implement a systematic, documented optimization process: identifying sources of dose, evaluating options for reduction (engineering controls, administrative controls, work planning), and implementing those that are reasonable given costs and benefits. It is not simply a goal of minimization — trade-offs between dose reduction and other factors (safety, reliability, cost) are explicitly considered.",
        difficulty=2,
        source="CNSC REGDOC-2.7.1; IAEA GSR Part 3"
    )

    add_question(db, 4,
        "What is the emergency reference level (ERL) concept used in nuclear emergency response?",
        [
            "The radiation level that triggers mandatory evacuation of the public",
            "A projected dose range within which a protective action (such as sheltering or evacuation) is considered appropriate, balancing dose reduction against disruption",
            "The maximum dose permitted to emergency workers responding to a nuclear accident",
            "The radiation level at which a nuclear facility must shut down"
        ],
        correct_index=1,
        explanation="Emergency Reference Levels (ERLs) — recommended by IAEA and ICRP — are projected dose ranges (e.g., 20-100 mSv) within which a specific protective action is generally warranted. They are not rigid triggers but decision-making tools that balance the radiation dose averted against the risks and disruption of the protective action. Decisions also consider actual field measurements, feasibility, and social factors.",
        difficulty=3,
        source="IAEA GSR Part 7; ICRP Publication 109"
    )

    # ── NUCLEAR SECURITY & SAFEGUARDS — add 10 more to reach 20 (cat id = 5) ─

    add_question(db, 5,
        "What is the difference between nuclear security and nuclear safety?",
        [
            "Nuclear security deals with radiation protection; nuclear safety deals with physical protection of facilities",
            "Nuclear security addresses intentional malicious acts; nuclear safety addresses unintentional failures and accidents",
            "Nuclear security is managed by military authorities; nuclear safety by civilian regulators",
            "There is no meaningful distinction — the terms refer to the same set of concerns"
        ],
        correct_index=1,
        explanation="Nuclear safety addresses the prevention of accidents and unintentional releases due to equipment failures, human error, or natural hazards. Nuclear security addresses the prevention of and response to intentional malicious acts — theft of nuclear material, sabotage of facilities, or radiological terrorism. While distinct, the two fields share common elements (physical barriers, access control) and must be coherently integrated.",
        difficulty=1,
        source="IAEA Nuclear Security Series"
    )

    add_question(db, 5,
        "What is nuclear smuggling and how does the IAEA's Incident and Trafficking Database (ITDB) address it?",
        [
            "Nuclear smuggling refers to unauthorized imports of nuclear technology; the ITDB tracks export control violations",
            "Nuclear smuggling involves unauthorized movement of nuclear or radioactive material; the ITDB collects and analyzes confirmed incidents to support member states' responses",
            "Nuclear smuggling is theoretical — no confirmed cases have occurred since the Cold War",
            "The ITDB is a classified database accessible only to nuclear weapon states"
        ],
        correct_index=1,
        explanation="Nuclear smuggling involves the unauthorized acquisition, movement, or transfer of nuclear or radioactive material. The IAEA's Incident and Trafficking Database (ITDB) collects information from participating member states on confirmed incidents of illicit trafficking, theft, loss, and unauthorized possession. Analysis of ITDB data informs nuclear security threat assessments and countermeasures.",
        difficulty=2,
        source="IAEA Nuclear Security Series No. 19"
    )

    add_question(db, 5,
        "What is the role of the Nuclear Security Summit process (2010-2016) in international nuclear security?",
        [
            "A series of IAEA-led summits establishing binding international nuclear security standards",
            "A series of world leader summits that significantly elevated political attention to nuclear security and accelerated material consolidation and security upgrades globally",
            "A UN Security Council process for sanctioning states with inadequate nuclear security",
            "A series of technical workshops for nuclear facility security managers"
        ],
        correct_index=1,
        explanation="The Nuclear Security Summit (NSS) process, initiated by US President Obama in 2010 with four summits (2010-2016), brought together world leaders to address nuclear security at the highest political level. The summits resulted in significant reductions in civilian stockpiles of highly enriched uranium, security upgrades at facilities worldwide, and strengthened international cooperation on nuclear security.",
        difficulty=2,
        source="Nuclear Security Summit Communiqués 2010-2016"
    )

    add_question(db, 5,
        "What is Canada's Comprehensive Nuclear Test Ban Treaty (CTBT) status and what does the treaty require?",
        [
            "Canada has not signed the CTBT",
            "Canada ratified the CTBT in 1998; the treaty prohibits all nuclear weapon test explosions and any other nuclear explosion",
            "Canada signed but not ratified the CTBT, meaning it is not legally bound",
            "Canada is exempt from CTBT requirements as a non-nuclear weapon state"
        ],
        correct_index=1,
        explanation="Canada ratified the Comprehensive Nuclear Test Ban Treaty (CTBT) in 1998. The CTBT prohibits all nuclear weapon test explosions and any other nuclear explosion. It established the Comprehensive Nuclear Test Ban Treaty Organization (CTBTO) to operate a global verification system including seismic, hydroacoustic, infrasound, and radionuclide monitoring. The treaty is not yet in force as some Annex 2 states have not ratified.",
        difficulty=2,
        source="CTBT; Global Affairs Canada"
    )

    add_question(db, 5,
        "What is a Design Information Questionnaire (DIQ) in IAEA safeguards?",
        [
            "A quality assurance document submitted by reactor vendors to the IAEA",
            "A document submitted by a state to the IAEA providing detailed design information about a nuclear facility subject to safeguards",
            "A checklist used by IAEA inspectors during routine facility inspections",
            "A report on the quantity of nuclear material produced at a facility"
        ],
        correct_index=1,
        explanation="A Design Information Questionnaire (DIQ) is submitted by a state to the IAEA for each nuclear facility subject to safeguards. It provides detailed information about the facility's design, nuclear material flows, containment points, and measurement systems. The IAEA uses this information to plan and conduct safeguards activities, including determining inspection access points and camera placement.",
        difficulty=2,
        source="IAEA INFCIRC/153"
    )

    add_question(db, 5,
        "What is the Physical Protection Convention (CPPNM) and its 2005 Amendment?",
        [
            "A voluntary IAEA guideline on nuclear facility security; the amendment made it mandatory",
            "A legally binding international convention on the physical protection of nuclear material; the 2005 amendment extended obligations to domestic use, storage, and transport and added sabotage provisions",
            "A bilateral treaty between the US and Russia on nuclear material protection",
            "An IAEA resolution on nuclear security that has not yet entered into force"
        ],
        correct_index=1,
        explanation="The Convention on the Physical Protection of Nuclear Material (CPPNM), in force since 1987, is the only legally binding international instrument on nuclear material physical protection. The 2005 Amendment (in force 2016) significantly strengthened it by extending obligations to domestically used, stored, and transported nuclear material, and adding requirements to protect nuclear facilities from sabotage.",
        difficulty=2,
        source="IAEA INFCIRC/274/Rev.1; 2005 Amendment"
    )

    add_question(db, 5,
        "What is meant by 'nuclear forensics' in the context of nuclear security?",
        [
            "The legal process for prosecuting nuclear smugglers in international courts",
            "Scientific analysis of nuclear or radiological material to determine its origin, history, and intended use following a security incident",
            "Background investigation of nuclear facility employees",
            "Reconstruction of historical nuclear weapon test data from atmospheric samples"
        ],
        correct_index=1,
        explanation="Nuclear forensics is the scientific analysis of intercepted nuclear or radiological material (or post-detonation debris) to determine its origin, history, and potential intended use. By analyzing isotopic composition, microstructure, chemical impurities, and other signatures, forensic analysis can help attribute material to its source — critical for law enforcement and deterrence following a nuclear security incident.",
        difficulty=2,
        source="IAEA Nuclear Security Series No. 2-G (Rev.1)"
    )

    add_question(db, 5,
        "What is the IAEA's Incident Response and Assistance Network (Iران) and when is it activated?",
        [
            "A standing IAEA military force for responding to nuclear facility attacks",
            "A network of member state experts and resources that can be rapidly mobilized to assist states in nuclear or radiological emergencies",
            "An automated monitoring system for detecting nuclear test explosions",
            "A financial mechanism for compensating states affected by transboundary nuclear contamination"
        ],
        correct_index=1,
        explanation="The IAEA Response and Assistance Network (RANET) — not IRAN — is a network of member states that have registered capabilities (teams, equipment, expertise) for responding to nuclear and radiological emergencies. When a state requests assistance under the Assistance Convention, IAEA can rapidly mobilize RANET resources from member states.",
        difficulty=2,
        source="IAEA INFCIRC/336"
    )

    add_question(db, 5,
        "What is the 'insider threat' in nuclear security and how is it mitigated?",
        [
            "The risk of cyberattacks originating from within a nuclear facility's computer network",
            "The threat posed by current or former employees who misuse their access, knowledge, or authority to commit theft or sabotage",
            "Safety risks from poorly trained workers making operational errors",
            "The risk of classified information being leaked to foreign governments"
        ],
        correct_index=1,
        explanation="The insider threat refers to the risk posed by individuals with authorized access — employees, contractors, or others — who might misuse that access to steal nuclear material or sabotage a facility. Mitigation measures include: trustworthiness determinations (background screening), two-person rules for sensitive activities, access controls, behavioral observation programs, and nuclear material accounting checks.",
        difficulty=2,
        source="IAEA Nuclear Security Series No. 8-G (Rev.1)"
    )

    add_question(db, 5,
        "What is 'nuclear security culture' and how does it relate to nuclear safety culture?",
        [
            "Nuclear security culture is a separate, unrelated concept from safety culture",
            "Both share the same underlying principles — leadership commitment, questioning attitude, and individual responsibility — applied to their respective domains of security and safety",
            "Safety culture is a regulatory requirement; security culture is voluntary",
            "Security culture applies only to security personnel; safety culture applies to all plant workers"
        ],
        correct_index=1,
        explanation="Nuclear security culture and nuclear safety culture share fundamental characteristics: demonstrated leadership commitment, individual accountability, a questioning attitude, and systematic processes. Both require that everyone — from senior management to frontline workers — recognizes their role and takes it seriously. Organizations are encouraged to integrate security and safety culture rather than treating them as competing concerns.",
        difficulty=2,
        source="IAEA Nuclear Security Series No. 7"
    )

    # ═══════════════════════════════════════════════════════════════════════
    # NEW CATEGORY: PWR REACTOR SYSTEMS (international)
    # ═══════════════════════════════════════════════════════════════════════

    pwr_id = add_category(db,
        "PWR Reactor Systems",
        "Pressurized water reactor design, systems, and safety features — internationally applicable",
        "🔵"
    )

    add_question(db, pwr_id,
        "What is the fundamental operating principle of a Pressurized Water Reactor (PWR)?",
        [
            "Water is allowed to boil in the reactor core, producing steam that drives the turbine directly",
            "Water is kept under high pressure to prevent boiling in the reactor core; heat is transferred to a secondary loop to produce steam",
            "Liquid sodium coolant transfers heat from the core to steam generators",
            "Heavy water moderator circulates through the core and directly drives a turbine"
        ],
        correct_index=1,
        explanation="In a PWR, the primary coolant is kept under high pressure (~15.5 MPa) to prevent boiling even at temperatures above 300°C. This hot pressurized water transfers its heat to a secondary loop through steam generators, where the secondary water flashes to steam to drive the turbine. The primary and secondary loops are physically separated, preventing radioactive primary water from reaching the turbine.",
        difficulty=1,
        source="IAEA Nuclear Power Reactor Characteristics"
    )

    add_question(db, pwr_id,
        "What is the function of the pressurizer in a PWR primary circuit?",
        [
            "It pumps primary coolant through the reactor core and steam generators",
            "It maintains the primary system pressure to prevent coolant boiling, using heaters and spray systems to control pressure",
            "It filters radioactive contamination from the primary coolant",
            "It controls the flow of feedwater to the steam generators"
        ],
        correct_index=1,
        explanation="The pressurizer is a tall vertical vessel connected to one primary loop hot leg. Electric heaters raise the water temperature to create a steam bubble that maintains system pressure (~15.5 MPa). Spray nozzles condense steam to reduce pressure when it rises too high. The pressurizer allows the primary system to respond to normal thermal expansion without damaging pressure excursions.",
        difficulty=2,
        source="IAEA-TECDOC-1234"
    )

    add_question(db, pwr_id,
        "What type of fuel does a typical PWR use?",
        [
            "Natural uranium dioxide (UO₂) pellets",
            "Low-enriched uranium dioxide (UO₂) pellets, typically 3-5% U-235",
            "Highly enriched uranium metal",
            "Mixed oxide (MOX) fuel in all fuel assemblies"
        ],
        correct_index=1,
        explanation="PWRs use low-enriched uranium (LEU) fuel pellets — uranium dioxide (UO₂) enriched to approximately 3-5% U-235, compared to natural uranium's 0.71%. Enrichment is necessary because light water absorbs more neutrons than heavy water, requiring more fissile material to sustain criticality. MOX (mixed uranium/plutonium oxide) fuel may be used in some assemblies in some plants.",
        difficulty=1,
        source="IAEA Nuclear Fuel Cycle"
    )

    add_question(db, pwr_id,
        "What is the role of boron in PWR reactor control?",
        [
            "Boron is used as a structural material in fuel assembly spacer grids",
            "Boric acid dissolved in the primary coolant provides long-term reactivity control and shutdown margin; concentration is adjusted throughout the fuel cycle",
            "Boron rods are inserted mechanically to shut down the reactor in an emergency",
            "Boron coatings on control rods improve their neutron absorption efficiency"
        ],
        correct_index=1,
        explanation="PWRs dissolve boric acid in the primary coolant for chemical shim control. At the start of a fuel cycle, boron concentration is high (~1200-1800 ppm) to compensate for excess reactivity; it is gradually diluted as fuel depletes. Emergency boration (rapid increase in boron concentration) is a shutdown mechanism. Soluble boron provides a uniform reactivity control mechanism throughout the core.",
        difficulty=2,
        source="IAEA Nuclear Reactor Theory"
    )

    add_question(db, pwr_id,
        "How many primary coolant loops does a typical large commercial PWR have, and what does each contain?",
        [
            "A single large loop containing the reactor, pump, and steam generator",
            "Two to four loops, each containing a reactor coolant pump and steam generator connected to a common reactor pressure vessel",
            "Six loops, each dedicated to a separate quadrant of the reactor core",
            "Two loops — one for normal operation and one as a backup"
        ],
        correct_index=1,
        explanation="Large commercial PWRs typically have 2-4 primary coolant loops (most large plants have 3 or 4). Each loop contains a reactor coolant pump (RCP) and a steam generator. All loops connect to the single reactor pressure vessel. Multiple loops provide redundancy and allow reduced-power operation with one loop isolated during maintenance.",
        difficulty=2,
        source="IAEA Nuclear Power Reactor Characteristics"
    )

    add_question(db, pwr_id,
        "What is a PWR steam generator and how does it work?",
        [
            "A direct-contact heat exchanger where primary and secondary water mix",
            "A large heat exchanger with thousands of small tubes carrying high-pressure primary water; secondary water on the shell side absorbs heat and produces steam",
            "A once-through boiler that converts all secondary feedwater to steam in a single pass",
            "A passive heat exchanger that requires no pumping — natural circulation drives flow"
        ],
        correct_index=1,
        explanation="A PWR steam generator is a large shell-and-tube heat exchanger. High-pressure radioactive primary water flows through thousands of small tubes (the tube bundle); lower-pressure secondary feedwater flows on the shell side, absorbing heat and producing steam. The tubes maintain separation between the radioactive primary and clean secondary circuits. Steam generator tube integrity is critical — tube failures allow radioactive primary water to contaminate the secondary side.",
        difficulty=1,
        source="IAEA Nuclear Power Reactor Characteristics"
    )

    add_question(db, pwr_id,
        "What is the Emergency Core Cooling System (ECCS) in a PWR and what does it do?",
        [
            "A backup electrical system that powers reactor coolant pumps during a station blackout",
            "A system that injects water into the reactor core to remove decay heat following a loss of coolant accident (LOCA)",
            "A passive system that cools the containment building exterior following an accident",
            "A system that provides makeup water to the pressurizer during normal operations"
        ],
        correct_index=1,
        explanation="The PWR ECCS consists of multiple subsystems providing core cooling following a LOCA: High-Pressure Injection System (HPIS) for small breaks, accumulators (passive nitrogen-pressurized tanks) for rapid injection during depressurization, and Low-Pressure Injection System (LPIS) for large breaks and long-term cooling. Multiple trains provide redundancy. The ECCS is a key design basis accident mitigation system.",
        difficulty=1,
        source="IAEA SSR-2/1"
    )

    add_question(db, pwr_id,
        "What is the negative temperature coefficient of reactivity in a PWR and why is it important?",
        [
            "A tendency for the reactor to become more reactive as temperature rises, requiring active control",
            "A safety characteristic where increasing coolant/fuel temperature automatically reduces reactivity, providing inherent self-regulation",
            "A measurement of the rate at which the reactor loses power during a trip",
            "A design requirement that control rods must insert within a specified time following a trip signal"
        ],
        correct_index=1,
        explanation="In PWRs, both the fuel Doppler coefficient and moderator temperature coefficient are negative — as temperature rises, reactivity decreases automatically. The Doppler effect (broadening of U-238 resonance absorption peaks with temperature) acts within microseconds. The moderator coefficient acts as water density decreases with temperature, reducing neutron moderation. This inherent negative feedback provides passive self-regulating safety behavior.",
        difficulty=2,
        source="IAEA Nuclear Reactor Theory; INSAG-12"
    )

    add_question(db, pwr_id,
        "What are the main design differences between a PWR and a VVER (Russian pressurized water reactor)?",
        [
            "VVERs use heavy water moderator while PWRs use light water",
            "VVERs use hexagonal fuel assemblies and horizontal steam generators in some older designs, while Western PWRs use square fuel assemblies and vertical steam generators",
            "VVERs operate at much lower pressure than Western PWRs",
            "VVERs and Western PWRs are functionally identical — only the manufacturer differs"
        ],
        correct_index=1,
        explanation="VVERs (Vodo-Vodyanoi Energetichesky Reaktor) are Russian-designed PWRs with key differences from Western designs: hexagonal fuel assemblies (vs. square), horizontal steam generators in older VVER-440 models (vs. vertical in Western designs and VVER-1000/1200), and different safety system designs. Modern VVER-1000 and VVER-1200 designs have largely converged with Western PWR concepts, including vertical steam generators.",
        difficulty=2,
        source="IAEA-TECDOC-1486"
    )

    add_question(db, pwr_id,
        "What is a reactor coolant pump (RCP) seal loss of coolant accident (SLOCA)?",
        [
            "A major pipe break in the primary coolant loop near the pump discharge",
            "A small LOCA caused by failure of the mechanical seals on a reactor coolant pump, resulting in primary water leakage",
            "Loss of coolant flow due to reactor coolant pump trip",
            "A loss of coolant accident affecting the secondary side cooling system"
        ],
        correct_index=1,
        explanation="RCP seal LOCAs occur when the multi-stage mechanical seals on a reactor coolant pump fail, allowing primary coolant to leak. Seal failures can result from loss of seal injection flow, loss of component cooling water, or mechanical degradation. Seal LOCAs are important design basis events — they are small LOCAs that require ECCS actuation and have been the initiating event in several significant plant incidents.",
        difficulty=3,
        source="IAEA Nuclear Power Plant Safety"
    )

    add_question(db, pwr_id,
        "What is the role of the containment building in a PWR nuclear power plant?",
        [
            "It is a decorative architectural feature with no safety function",
            "It is the final barrier preventing release of radioactive material to the environment; it must remain intact and leaktight following design basis accidents",
            "It provides structural support for the turbine building",
            "It is used solely for radiation shielding during normal operations"
        ],
        correct_index=1,
        explanation="The PWR containment building is a robust reinforced concrete and/or steel structure housing the reactor pressure vessel, primary circuit, and associated systems. Following a LOCA or other accident, it contains steam, water, and radioactive material released from the primary circuit. Containment integrity is maintained by design features and active systems (containment spray, fan coolers) to limit pressure and temperature buildup.",
        difficulty=1,
        source="IAEA SSR-2/1"
    )

    add_question(db, pwr_id,
        "What is a Loss of Feedwater (LOFW) event and why is it a concern for PWR operations?",
        [
            "Loss of feedwater to the secondary side of steam generators, which reduces heat removal from the primary circuit and can lead to primary overpressurization",
            "Loss of cooling water to reactor coolant pump motors, causing pump trip",
            "Loss of borated water injection to the reactor core",
            "Loss of water supply to the spent fuel pool"
        ],
        correct_index=0,
        explanation="A Loss of Feedwater event occurs when feedwater flow to the steam generators is lost, reducing secondary-side heat removal. This causes the primary coolant to heat up, increasing pressure. Reactor trip occurs on high coolant temperature or pressure. Auxiliary feedwater systems (AFW) are designed to provide makeup water to the steam generators to restore heat removal capability.",
        difficulty=2,
        source="IAEA Nuclear Power Plant Safety"
    )

    add_question(db, pwr_id,
        "What international organizations develop safety standards specifically applied to PWR design and operation?",
        [
            "Only the IAEA develops internationally applicable PWR standards",
            "The IAEA, WENRA (Western European Nuclear Regulators Association), and national regulators all contribute standards applicable to PWRs internationally",
            "Only national regulators develop applicable standards; there are no international PWR-specific standards",
            "The World Association of Nuclear Operators (WANO) develops all international PWR safety standards"
        ],
        correct_index=1,
        explanation="Multiple organizations contribute to international PWR safety standards: the IAEA through its Safety Standards Series (SSR-2/1 for design, SSR-2/2 for safety of research reactors); WENRA through reactor harmonization working groups for European regulators; and national regulators who adopt and adapt these standards. WANO provides operational performance peer reviews but does not develop regulatory standards.",
        difficulty=2,
        source="IAEA SSR-2/1; WENRA"
    )

    add_question(db, pwr_id,
        "What is a station blackout (SBO) and why is it a key design concern for PWRs?",
        [
            "A planned electrical outage to the plant during which reactor shutdown is required",
            "Loss of all AC power to the plant — loss of grid plus failure of backup diesel generators — potentially compromising safety system operation",
            "Loss of power to the control room instrumentation and control systems only",
            "A condition in which the reactor shuts down due to loss of the electrical load"
        ],
        correct_index=1,
        explanation="A Station Blackout (SBO) is the loss of all alternating current (AC) power — loss of offsite grid power combined with failure of all onsite diesel generators. SBO was the key initiating condition at Fukushima Daiichi. PWR safety systems require AC power for pumps and valves; SBO can compromise core cooling. Post-Fukushima requirements include extended SBO coping capability using battery-backed systems and portable equipment.",
        difficulty=2,
        source="IAEA Safety Reports Series; Post-Fukushima Action Plans"
    )

    add_question(db, pwr_id,
        "What PWR safety system uses passive natural circulation to remove decay heat without pumps or external power?",
        [
            "The emergency core cooling system high-pressure injection trains",
            "Passive residual heat removal systems (PRHRS) or passive safety systems in advanced PWR designs such as AP1000",
            "The reactor coolant pump flywheel coastdown",
            "The pressurizer relief and safety valves"
        ],
        correct_index=1,
        explanation="Advanced PWR designs like the Westinghouse AP1000 and SNPTC CAP1400 use passive safety systems that rely on gravity, natural circulation, and compressed gas rather than pumps and AC power. The Passive Residual Heat Removal System (PRHRS) removes decay heat through natural convection to an elevated tank of water, providing cooling for 72 hours without operator action or AC power.",
        difficulty=3,
        source="IAEA Advanced Reactor Designs"
    )

    add_question(db, pwr_id,
        "What are typical capacity factors for modern PWR nuclear power plants?",
        [
            "30-50%, due to frequent refuelling outages every 3 months",
            "70-95%, with modern plants regularly exceeding 90% through extended fuel cycles and improved outage management",
            "50-65%, due to mandatory weekly testing of safety systems",
            "Less than 30%, because safety regulations require extensive planned downtime"
        ],
        correct_index=1,
        explanation="Modern PWRs achieve high capacity factors — typically 85-95% — through 18-24 month fuel cycles (reducing outage frequency), improved outage planning and execution, and better reliability programs. Many plants regularly exceed 90% annual capacity factor. The industry average has improved significantly since the 1980s due to operational excellence programs championed by WANO and INPO.",
        difficulty=1,
        source="IAEA PRIS Database"
    )

    add_question(db, pwr_id,
        "What is the significance of zirconium cladding in PWR fuel and what failure mechanism became important at Fukushima?",
        [
            "Zirconium is used for its neutron absorption properties; at Fukushima it absorbed excess neutrons preventing criticality",
            "Zirconium alloy cladding has low neutron absorption and good corrosion resistance; at high temperatures (>1200°C) it reacts with steam to produce hydrogen, which ignited at Fukushima",
            "Zirconium cladding provides structural rigidity to fuel assemblies; at Fukushima it prevented fuel collapse",
            "Zirconium is used for its thermal conductivity; at Fukushima it helped conduct decay heat away from the core"
        ],
        correct_index=1,
        explanation="Zirconium alloys (Zircaloy, ZIRLO, M5) are used for fuel rod cladding because of their low thermal neutron absorption cross-section and good corrosion resistance in hot water. At high temperatures during severe accidents (>1200°C), zirconium reacts with steam: Zr + 2H₂O → ZrO₂ + 2H₂. The hydrogen produced at Fukushima Daiichi Units 1, 3, and 4 accumulated and exploded, damaging reactor buildings.",
        difficulty=2,
        source="IAEA Fukushima Daiichi Report"
    )

    add_question(db, pwr_id,
        "What is refuelling frequency for a typical PWR and how does it compare to a CANDU reactor?",
        [
            "PWRs refuel every week; CANDU refuels monthly",
            "PWRs refuel every 12-24 months during a planned shutdown outage; CANDU refuels continuously at full power",
            "PWRs and CANDU both refuel during planned outages every 18 months",
            "PWRs refuel daily through an automated system; CANDU refuels annually"
        ],
        correct_index=1,
        explanation="PWRs shut down for refuelling every 12-24 months (typically 18 months for modern plants), replacing about one-third of the core at each outage. CANDU reactors refuel continuously at full power using fuelling machines, eliminating refuelling outages. This gives CANDU a potential capacity factor advantage but requires the more complex fuelling machine systems and on-power refuelling capability.",
        difficulty=1,
        source="IAEA Nuclear Power Reactor Characteristics"
    )

    add_question(db, pwr_id,
        "What is the function of control rods in a PWR?",
        [
            "They provide structural support for the fuel assemblies in the core",
            "They absorb neutrons to control reactor power level and provide shutdown capability; they are inserted from the top of the reactor vessel",
            "They circulate coolant through the reactor core by rotation",
            "They measure neutron flux distribution within the reactor core"
        ],
        correct_index=1,
        explanation="PWR control rods are clusters of neutron-absorbing material (typically hafnium, Ag-In-Cd, or boron carbide) that are inserted into guide tubes within fuel assemblies from above. They control reactor power during operation (via partial insertion) and provide rapid shutdown (reactor trip/SCRAM) when fully inserted. PWRs also use soluble boron for long-term reactivity control, reducing reliance on control rods during normal operation.",
        difficulty=1,
        source="IAEA Nuclear Reactor Theory"
    )

    add_question(db, pwr_id,
        "What is a pressurized thermal shock (PTS) event and why is it important for PWR reactor pressure vessel integrity?",
        [
            "A temperature shock applied to fuel pellets during rapid power changes",
            "Rapid cooling of the reactor pressure vessel wall during certain accidents, which can cause thermal stresses that challenge vessel integrity in older embrittled vessels",
            "Overpressurization of the primary system during a steam generator tube rupture",
            "Thermal stratification in the pressurizer during low-power operations"
        ],
        correct_index=1,
        explanation="Pressurized Thermal Shock (PTS) occurs during certain accidents (e.g., ECCS injection during a LOCA) when cold water rapidly cools the reactor pressure vessel wall while it remains under high pressure. If the vessel material is embrittled by neutron irradiation (as it becomes in older plants), the thermal stress can potentially cause brittle fracture. PTS is a key aging management concern for PWR life extension.",
        difficulty=3,
        source="IAEA Safety Reports Series No. 54"
    )

    # ═══════════════════════════════════════════════════════════════════════
    # NEW CATEGORY: BWR REACTOR SYSTEMS (international)
    # ═══════════════════════════════════════════════════════════════════════

    bwr_id = add_category(db,
        "BWR Reactor Systems",
        "Boiling water reactor design, systems, and safety features — internationally applicable",
        "💧"
    )

    add_question(db, bwr_id,
        "What is the fundamental operating principle of a Boiling Water Reactor (BWR)?",
        [
            "Water is kept under pressure to prevent boiling; a separate secondary loop produces steam",
            "Water is allowed to boil directly in the reactor core; the steam produced drives the turbine directly without a secondary loop",
            "Heavy water is used as coolant and allowed to boil; light water provides the secondary steam supply",
            "Liquid metal coolant transfers heat from the core to a steam generator in a secondary loop"
        ],
        correct_index=1,
        explanation="In a BWR, the primary coolant is allowed to boil within the reactor core at a pressure of approximately 7 MPa (~1000 psi). The steam produced in the core rises through moisture separators and steam dryers and goes directly to the turbine without a separate secondary loop. This eliminates steam generators but means the turbine handles slightly radioactive steam.",
        difficulty=1,
        source="IAEA Nuclear Power Reactor Characteristics"
    )

    add_question(db, bwr_id,
        "How does a BWR control reactor power during normal operations?",
        [
            "Primarily through control rod insertion from below and adjustment of recirculation flow rate",
            "Through soluble boron concentration in the coolant and control rod position",
            "Through adjustment of primary coolant pump speed only",
            "Through variable feedwater temperature control"
        ],
        correct_index=0,
        explanation="BWRs use two main mechanisms for power control: (1) Control rods inserted from below the core (due to steam in the upper core region), and (2) Recirculation flow control — increasing recirculation pump speed increases core flow, sweeping out steam voids and increasing reactivity and power. Flow control allows rapid power changes without moving control rods, making BWRs responsive to load following.",
        difficulty=2,
        source="IAEA Nuclear Reactor Theory"
    )

    add_question(db, bwr_id,
        "What is the void coefficient of reactivity in a BWR and what is its safety significance?",
        [
            "A positive coefficient meaning that more steam voids increase reactor power — requiring careful operator control",
            "A strongly negative coefficient meaning that increasing steam voids (bubbles) in the core reduce reactivity, providing inherent self-regulation",
            "A neutral coefficient meaning steam voids have no effect on BWR reactor power",
            "A coefficient that varies from positive to negative depending on core burnup"
        ],
        correct_index=1,
        explanation="The BWR void coefficient is strongly negative — as more steam voids form in the core (due to increased power or reduced pressure), reactivity decreases automatically. This is a key inherent safety characteristic: if power rises, more boiling occurs, which reduces reactivity and limits further power rise. This self-regulating behavior is fundamental to BWR safety.",
        difficulty=2,
        source="IAEA Nuclear Reactor Theory"
    )

    add_question(db, bwr_id,
        "What is the Mark I containment and which reactor type uses it?",
        [
            "A large dry containment structure used in early PWR designs",
            "A pressure-suppression containment used in GE BWRs featuring a drywell and a torus-shaped wetwell with suppression pool",
            "A steel containment sphere used in early CANDU designs",
            "A containment design that proved inadequate at Three Mile Island"
        ],
        correct_index=1,
        explanation="The Mark I containment is a pressure-suppression design used in early General Electric BWRs. It consists of a light bulb-shaped drywell (containing the reactor vessel) connected to a torus-shaped suppression pool (wetwell). Steam from a pipe break is directed into the suppression pool where it condenses, limiting pressure buildup. Three Fukushima Daiichi units (1, 2, 3) had Mark I containments, which faced challenges managing hydrogen and pressure during the accident.",
        difficulty=2,
        source="IAEA Fukushima Daiichi Report"
    )

    add_question(db, bwr_id,
        "What is the Isolation Condenser (IC) system in early BWR designs?",
        [
            "A system that isolates the BWR primary circuit from the turbine during a steam line break",
            "A passive heat removal system that removes decay heat by condensing steam from the reactor vessel when the plant is isolated from the main condenser",
            "A system that condenses steam from the suppression pool during a LOCA",
            "The secondary condenser used to cool turbine exhaust steam in BWR plants"
        ],
        correct_index=1,
        explanation="The Isolation Condenser (IC) is a passive heat removal system in older BWR designs (e.g., BWR/3 and some BWR/4). When the reactor is isolated from the main condenser (e.g., due to turbine trip or MSIV closure), the IC condenses steam from the reactor vessel and returns condensate by gravity, removing decay heat without pumps or AC power. Fukushima Unit 1 had an IC that was not properly operated during the accident.",
        difficulty=3,
        source="IAEA Fukushima Daiichi Report"
    )

    add_question(db, bwr_id,
        "What is the Reactor Core Isolation Cooling (RCIC) system in a BWR?",
        [
            "A safety system that isolates the reactor core from coolant flow during a LOCA",
            "A turbine-driven pump system that injects water into the reactor vessel using steam from the reactor itself, operating without AC power",
            "A passive system using gravity-fed tanks to provide core cooling",
            "A system that monitors reactor core temperature during isolation events"
        ],
        correct_index=1,
        explanation="RCIC is a key BWR safety system consisting of a turbine-driven pump powered by reactor steam itself (not AC electricity). When the reactor is isolated from the main feedwater, RCIC injects water from the condensate storage tank or suppression pool into the reactor vessel to maintain water level and remove decay heat. RCIC systems operated at Fukushima units for varying periods during the accident.",
        difficulty=2,
        source="IAEA Fukushima Daiichi Report"
    )

    add_question(db, bwr_id,
        "Why are BWR control rods inserted from below the core, unlike PWR control rods?",
        [
            "BWR control rods are heavier and require hydraulic pressure from below to insert them against gravity",
            "The upper core region contains steam which makes control rod guide tube design from above impractical; hydraulic insertion from below allows fine positioning",
            "Inserting from below allows control rods to be inserted more quickly in an emergency",
            "This is simply a historical design convention with no technical basis"
        ],
        correct_index=1,
        explanation="In a BWR, the upper portion of the core contains a significant steam void fraction. Placing control rod drive mechanisms below the core avoids the steam region and allows more compact guide tube design. BWR control rods are inserted upward using hydraulic pressure (fine motion control rod drives in modern designs). Emergency shutdown uses both hydraulic insertion and spring-loaded mechanisms for rapid SCRAM.",
        difficulty=2,
        source="IAEA Nuclear Reactor Theory"
    )

    add_question(db, bwr_id,
        "What does ABWR stand for and what key improvements does it offer over earlier BWR designs?",
        [
            "Advanced British Water Reactor — a UK development of the BWR concept with horizontal steam generators",
            "Advanced Boiling Water Reactor — improved safety systems including internal recirculation pumps, passive safety features, and simplified plant design",
            "Automated Boiling Water Reactor — a fully automated BWR with no manual operator controls",
            "Auxiliary Boiling Water Reactor — a smaller BWR used for industrial heat supply"
        ],
        correct_index=1,
        explanation="The ABWR (Advanced Boiling Water Reactor), developed by GE-Hitachi and Toshiba, incorporates significant improvements over older BWR designs: internal recirculation pumps (eliminating large external recirculation piping — a major LOCA source), fine motion control rod drives, improved emergency core cooling, digital instrumentation and control, and passive safety features. ABWRs operate in Japan and are licensed in several other countries.",
        difficulty=2,
        source="IAEA Advanced Reactor Designs"
    )

    add_question(db, bwr_id,
        "What is the Main Steam Isolation Valve (MSIV) and why is it critical in BWR design?",
        [
            "A valve that controls steam flow to the turbine during load changes",
            "A large isolation valve on each main steam line that closes rapidly to isolate the reactor from the turbine and prevent uncontrolled steam release during accidents",
            "A pressure relief valve that opens to prevent primary system overpressurization",
            "A valve that diverts main steam to the condenser during turbine bypass"
        ],
        correct_index=1,
        explanation="MSIVs are large, fast-acting valves located on each main steam line inside and outside the primary containment. They close within seconds on signals indicating steam line breaks or other accidents, isolating the reactor from the turbine and preventing uncontrolled release of radioactive steam. MSIV closure is a common initiating event for BWR transients since it suddenly removes the main heat removal pathway.",
        difficulty=2,
        source="IAEA Nuclear Power Plant Safety"
    )

    add_question(db, bwr_id,
        "How does the BWR suppression pool contribute to safety?",
        [
            "It stores emergency diesel fuel for backup power systems",
            "It condenses steam released from the primary circuit during accidents, limiting containment pressure, and provides a water source for emergency core cooling",
            "It provides a physical barrier between the reactor building and the environment",
            "It stores spent fuel rods after removal from the reactor core"
        ],
        correct_index=1,
        explanation="The suppression pool (wetwell) contains large volumes of water that perform several safety functions: it condenses steam vented from the drywell during a LOCA or other accident (pressure suppression), limiting containment pressure buildup; it provides a source of water for ECCS and RCIC systems; and in some designs it serves as a heat sink for passive decay heat removal. Pool temperature management is an important operational consideration during accidents.",
        difficulty=2,
        source="IAEA Nuclear Power Plant Safety"
    )

    add_question(db, bwr_id,
        "In what countries are BWRs predominantly operated today?",
        [
            "BWRs are operated only in the United States",
            "BWRs are operated primarily in Japan, the United States, Sweden, Finland, Germany (historically), Mexico, Spain, and Taiwan",
            "BWRs are the dominant reactor type globally, operated in over 30 countries",
            "BWRs are operated only in Japan and the United States following their phase-out elsewhere"
        ],
        correct_index=1,
        explanation="BWRs were developed by General Electric and are operated primarily in: Japan (many units, though most are offline post-Fukushima), the United States (~34 units), Sweden, Finland, Spain, Mexico, Taiwan, and India (BWR-220 design). Germany had several BWRs but phased out nuclear power in 2023. They represent about 20% of the world's operating nuclear power capacity.",
        difficulty=1,
        source="IAEA PRIS Database"
    )

    add_question(db, bwr_id,
        "What is the key safety lesson from the Fukushima Daiichi accident specifically related to BWR design?",
        [
            "BWRs are fundamentally unsafe and should be replaced with PWRs",
            "Station blackout combined with tsunami beyond design basis led to loss of all core cooling; post-Fukushima actions focus on diverse and flexible coping strategies (FLEX) for beyond-design-basis events",
            "The Mark I containment failed completely, requiring replacement with large dry containments",
            "Control rod insertion failed at all three damaged units, leading to uncontrolled power excursions"
        ],
        correct_index=1,
        explanation="The Fukushima accident demonstrated the vulnerability of nuclear plants to beyond-design-basis external events and the importance of extended loss of AC power coping capability. Post-Fukushima corrective actions worldwide include: diverse portable power and pumping equipment (FLEX), enhanced spent fuel pool instrumentation, filtered containment venting systems, improved hydrogen management, and strengthened emergency operating procedures for beyond-design-basis conditions.",
        difficulty=2,
        source="IAEA Fukushima Daiichi Report; WANO Post-Fukushima Good Practices"
    )

    add_question(db, bwr_id,
        "What is the function of the moisture separator and steam dryer in a BWR?",
        [
            "They remove dissolved minerals from the feedwater before it enters the reactor core",
            "They separate water droplets from the steam produced in the core before it reaches the turbine, improving turbine efficiency and protecting turbine blades",
            "They filter radioactive contamination from the steam before it reaches the turbine",
            "They control the ratio of steam to water in the core to maintain proper void fraction"
        ],
        correct_index=1,
        explanation="Steam produced in the BWR core contains water droplets (wet steam). Moisture separators spin the steam to remove large droplets; steam dryers (corrugated metal sheets) remove finer droplets. Delivering dry steam to the turbine is essential for turbine efficiency and to protect turbine blades from erosion by water droplets. Steam quality (dryness fraction) is an important BWR operational parameter.",
        difficulty=2,
        source="IAEA Nuclear Power Reactor Characteristics"
    )

    add_question(db, bwr_id,
        "What is a BWR stability concern and how is it managed?",
        [
            "BWRs are prone to pressure vessel cracking under cyclic loading; managed through regular ultrasonic testing",
            "BWRs can experience coupled neutronics-thermal-hydraulic oscillations (power/flow instability) at certain low-flow, high-power conditions; managed through operating restrictions and monitoring systems",
            "BWRs experience fuel melting during rapid power ramps; managed through power rate limits",
            "BWRs are prone to control rod ejection accidents; managed through control rod drive testing"
        ],
        correct_index=1,
        explanation="BWR instability refers to coupled neutronics-thermal-hydraulic oscillations that can occur at certain operating conditions — typically low recirculation flow and high power. Density wave oscillations in fuel channels interact with the void coefficient to produce power oscillations. This led to an incident at LaSalle Unit 2 (1988). BWRs are managed through restricted operating regions, exclusion zones on power-flow maps, and oscillation detection and suppression systems.",
        difficulty=3,
        source="IAEA Nuclear Power Plant Safety"
    )

    add_question(db, bwr_id,
        "What is the typical thermal efficiency of a BWR compared to a PWR and what determines this?",
        [
            "BWRs are significantly less efficient (~25%) than PWRs (~35%) due to energy losses in steam separation",
            "BWRs and PWRs have similar thermal efficiencies (~33-37%); BWRs have a slight disadvantage due to lower steam conditions but save the steam generator energy loss",
            "BWRs are more efficient (~45%) because they operate at higher temperatures",
            "Thermal efficiency is identical for all light water reactor types at exactly 33%"
        ],
        correct_index=1,
        explanation="BWRs and PWRs have similar thermal efficiencies (~33-37%). BWR steam conditions (7 MPa, ~285°C) are lower than PWR secondary steam conditions (~6-7 MPa), slightly reducing Rankine cycle efficiency. However, BWRs eliminate the PWR steam generator energy transfer losses. Modern advanced designs in both types achieve similar efficiencies around 33-36%.",
        difficulty=3,
        source="IAEA Nuclear Power Reactor Characteristics"
    )

    add_question(db, bwr_id,
        "What is the ESBWR and how does it differ from conventional BWR designs?",
        [
            "The European Standard BWR — a BWR design standardized for European regulatory requirements",
            "The Economic Simplified BWR (GE-Hitachi) — a Generation IV design using entirely passive safety systems requiring no AC power or pumps for core cooling for 72+ hours",
            "The Enhanced Safety BWR — a retrofitted older BWR with improved ECCS",
            "The Extended Steam BWR — a larger BWR design with more steam generators"
        ],
        correct_index=1,
        explanation="The ESBWR (Economic Simplified Boiling Water Reactor), developed by GE-Hitachi, is a Generation III+ passive design. It uses entirely passive safety systems: the Gravity-Driven Cooling System (GDCS), Passive Containment Cooling System (PCCS), and Isolation Condensers for decay heat removal — all without AC power or pumps. The ESBWR is licensed by the US NRC and represents the advanced evolution of BWR technology.",
        difficulty=3,
        source="IAEA Advanced Reactor Designs"
    )

    add_question(db, bwr_id,
        "What is General Electric's contribution to BWR development and which generations of BWRs exist?",
        [
            "GE developed only the first generation; subsequent designs were developed by national governments",
            "GE (now GE-Hitachi) developed BWRs from the 1950s through six product generations (BWR/1 through BWR/6), with the ABWR and ESBWR as advanced successors",
            "BWRs were originally developed by Westinghouse and acquired by GE in the 1970s",
            "GE developed three generations of BWRs before discontinuing the product line in the 1990s"
        ],
        correct_index=1,
        explanation="General Electric developed the BWR concept from the 1950s. Six product generations followed: BWR/1 (prototype, Dresden-1), through BWR/6 (the most common, incorporating improved ECCS and containment). GE then developed the ABWR with Japanese partners (operating in Japan since 1996), followed by the passive ESBWR. GE-Hitachi Nuclear Energy currently markets both designs internationally.",
        difficulty=2,
        source="IAEA Nuclear Power Reactor Characteristics"
    )

    add_question(db, bwr_id,
        "What radiological challenge is unique to BWR turbines compared to PWR turbines?",
        [
            "BWR turbines operate at higher radiation levels because primary coolant steam flows directly through the turbine, causing N-16 and activation product deposition",
            "BWR turbines have higher radiation levels due to higher fuel enrichment",
            "BWR turbines require more frequent inspection than PWR turbines due to higher temperatures",
            "There is no radiological difference between BWR and PWR turbines"
        ],
        correct_index=0,
        explanation="Because BWR steam goes directly from the reactor to the turbine without an intermediate steam generator, the turbine handles radioactive primary steam. N-16 (produced by neutron activation of O-16, t½ = 7.1 sec) creates significant dose rates in the turbine building during operation. Additionally, activated corrosion products (Co-58, Co-60, Cs-134, Cs-137) deposit on turbine components, requiring extensive radiation protection measures during maintenance.",
        difficulty=2,
        source="IAEA Radiation Protection in Nuclear Power Plants"
    )

    # ═══════════════════════════════════════════════════════════════════════
    # NEW CATEGORY: INPO AND WANO
    # ═══════════════════════════════════════════════════════════════════════

    wano_id = add_category(db,
        "INPO and WANO",
        "Institute of Nuclear Power Operations and World Association of Nuclear Operators — nuclear excellence programs",
        "🌟"
    )

    add_question(db, wano_id,
        "What event prompted the creation of INPO (Institute of Nuclear Power Operations) and when was it established?",
        [
            "The Chernobyl accident in 1986 prompted US utilities to form a self-regulatory body",
            "The Three Mile Island accident in 1979 led US nuclear utilities to establish INPO in 1979 to improve nuclear plant operational safety",
            "INPO was established by the US Nuclear Regulatory Commission in 1975 as an industry oversight body",
            "INPO was formed in 1990 following concerns about declining nuclear plant capacity factors"
        ],
        correct_index=1,
        explanation="INPO was established in 1979 by the US nuclear power industry in direct response to the Three Mile Island Unit 2 accident. The industry recognized that it needed to take responsibility for nuclear excellence rather than relying solely on regulation. INPO was founded to promote the highest levels of safety and reliability through evaluations, training, information sharing, and assistance.",
        difficulty=1,
        source="INPO Historical Background"
    )

    add_question(db, wano_id,
        "What is WANO and how does it relate to INPO?",
        [
            "WANO is a regulatory body that oversees INPO's activities internationally",
            "WANO (World Association of Nuclear Operators) was established in 1989 after Chernobyl to extend the INPO model globally, bringing together nuclear operators from all countries including those with different political systems",
            "WANO is the European equivalent of INPO, operating independently in EU member states",
            "WANO replaced INPO in 1989 as the primary nuclear industry oversight organization"
        ],
        correct_index=1,
        explanation="WANO (World Association of Nuclear Operators) was established in 1989 following the Chernobyl accident, which demonstrated that a nuclear accident anywhere affects the entire global industry. WANO extended the INPO model internationally, creating a global peer review and excellence program that includes operators from all countries — including those with different political and regulatory systems. INPO continues to operate as WANO's US regional center.",
        difficulty=1,
        source="WANO Historical Background"
    )

    add_question(db, wano_id,
        "What are the four regional centres of WANO?",
        [
            "North America, Europe, Asia, and the Middle East",
            "Atlanta (Americas), Paris (Europe/Africa), Moscow (Eastern Europe/FSU), and Tokyo (Asia-Pacific)",
            "Washington, London, Paris, and Beijing",
            "North America, Western Europe, Eastern Europe, and Asia-Pacific"
        ],
        correct_index=1,
        explanation="WANO operates through four regional centres: Atlanta, Georgia (serving the Americas — effectively INPO); Paris, France (serving Western and Central Europe, Africa, and the Middle East); Moscow, Russia (serving Eastern Europe and former Soviet Union states); and Tokyo, Japan (serving Asia-Pacific). A coordinating centre is based in London.",
        difficulty=2,
        source="WANO Organizational Structure"
    )

    add_question(db, wano_id,
        "What is a WANO Peer Review and what does it assess?",
        [
            "A financial audit of nuclear power plant operating costs conducted by WANO staff",
            "A comprehensive review of a nuclear plant's operational safety and performance conducted by a team of experienced nuclear professionals from other organizations against WANO good practices",
            "A regulatory inspection conducted by WANO on behalf of national nuclear regulators",
            "An engineering review of nuclear plant design modifications"
        ],
        correct_index=1,
        explanation="A WANO Peer Review is a systematic assessment of a nuclear plant's operational safety performance conducted by a team of experienced nuclear professionals from other member organizations. It evaluates against WANO Good Practices across all areas of plant operations and identifies areas for improvement (AFIs). Unlike regulatory inspections, peer reviews are collaborative — the goal is mutual improvement, not enforcement.",
        difficulty=1,
        source="WANO Peer Review Guidelines"
    )

    add_question(db, wano_id,
        "What are WANO Performance Indicators (PIs) and how are they used?",
        [
            "Financial metrics used to assess the economic performance of nuclear power plants",
            "Standardized operational metrics (such as unit capability factor, fuel reliability, and unplanned automatic scrams) that allow comparison of plant performance across the global nuclear fleet",
            "Regulatory compliance metrics reported to national regulators by all WANO member plants",
            "Safety metrics required by the IAEA for all nuclear power plants worldwide"
        ],
        correct_index=1,
        explanation="WANO Performance Indicators are a standardized set of operational metrics tracked across the global nuclear fleet. They include: Unit Capability Factor, Unplanned Capability Loss Factor, Unplanned Automatic Scrams per 7000 hours, Safety System Actuations, Fuel Reliability, Chemistry Index, Collective Radiation Exposure, and Industrial Safety Accident Rate. PIs allow operators to benchmark their performance against world median and world class levels.",
        difficulty=2,
        source="WANO Performance Indicators Program"
    )

    add_question(db, wano_id,
        "What is INPO's SALP program and what did it assess?",
        [
            "Safety Assessment of Licensed Plants — INPO's formal rating system for US nuclear plants that was replaced by the Reactor Oversight Process",
            "Systematic Assessment of Licensee Performance — a program INPO ran jointly with the NRC until 1999",
            "Safety Analysis of Large Plants — a technical safety review program for plants above 1000 MWe",
            "INPO never had a SALP program — this was run by the NRC only"
        ],
        correct_index=3,
        explanation="SALP (Systematic Assessment of Licensee Performance) was actually an NRC program — not INPO — that assessed US nuclear plant performance from 1979 to 1999. It was replaced by the NRC's Reactor Oversight Process (ROP). INPO conducts its own separate evaluation program using INPO evaluations and Assist Visits, independent of the NRC's oversight activities.",
        difficulty=3,
        source="NRC; INPO Programs"
    )

    add_question(db, wano_id,
        "What is the WANO Operational Experience (OE) program?",
        [
            "A program that archives historical nuclear plant operating records for research purposes",
            "A program that collects, analyzes, and disseminates lessons learned from significant events at nuclear plants worldwide to prevent recurrence at other plants",
            "A qualification program for nuclear plant operators",
            "A program that tracks the career history of nuclear plant senior managers"
        ],
        correct_index=1,
        explanation="WANO's Operational Experience (OE) program collects information on significant events, near-misses, and good practices from member organizations worldwide, analyzes them for broader applicability, and disseminates lessons to all members through Operating Experience Reports (OERs) and other communications. This global sharing of operational experience helps prevent recurrence of events and spreads good practices across the entire industry.",
        difficulty=1,
        source="WANO Operational Experience Program"
    )

    add_question(db, wano_id,
        "What is INPO's role in US nuclear plant training and accreditation?",
        [
            "INPO accredits all nuclear plant training programs in the US, ensuring they meet standards for operator and maintenance training",
            "INPO provides optional training consulting services but has no accreditation role",
            "INPO training accreditation was transferred to the NRC in 2000",
            "INPO accredits only senior reactor operator training programs; other training is unaccredited"
        ],
        correct_index=0,
        explanation="INPO accredits nuclear power plant training programs across all disciplines — licensed operator training, maintenance, radiation protection, chemistry, and engineering — through a systematic accreditation process based on the Systematic Approach to Training (SAT). Accreditation requires regular reviews and maintains training quality standards across the US industry. The NRC requires that licensed operator training meet INPO accreditation standards.",
        difficulty=2,
        source="INPO Accreditation Program"
    )

    add_question(db, wano_id,
        "What is the purpose of a WANO Technical Support Mission (TSM)?",
        [
            "A mission where WANO staff take over management of a poorly performing nuclear plant",
            "A focused assistance visit where WANO provides expert support to a member organization addressing a specific technical or operational challenge",
            "A technical inspection required before a plant can restart following a major outage",
            "A mission where WANO collects performance data for benchmarking purposes"
        ],
        correct_index=1,
        explanation="A WANO Technical Support Mission (TSM) is a targeted assistance activity where WANO provides a small team of experts to help a member organization address a specific technical, operational, or programmatic challenge. Unlike a full peer review, a TSM is narrowly focused on a particular issue — for example, improving corrective action program effectiveness, outage management, or equipment reliability — at the member's request.",
        difficulty=2,
        source="WANO Support Programs"
    )

    add_question(db, wano_id,
        "What is nuclear safety culture as defined by INSAG (International Nuclear Safety Advisory Group) and used by WANO and INPO?",
        [
            "The formal safety management system implemented at a nuclear power plant",
            "That assembly of characteristics and attitudes in organizations and individuals which establishes that — as an overriding priority — nuclear plant safety issues receive the attention warranted by their significance",
            "The collection of safety regulations and procedures governing nuclear plant operations",
            "The attitude of nuclear plant workers toward their personal radiation protection"
        ],
        correct_index=1,
        explanation="INSAG-4 (1991) defined safety culture as 'that assembly of characteristics and attitudes in organizations and individuals which establishes that, as an overriding priority, nuclear plant safety issues receive the attention warranted by their significance.' This definition, widely adopted by WANO, INPO, the IAEA, and CNSC, emphasizes both organizational and individual dimensions — safety culture is not just procedures and systems but the values and behaviors that prioritize safety.",
        difficulty=2,
        source="INSAG-4; WANO Safety Culture Assessment"
    )

    add_question(db, wano_id,
        "What does WANO's 'nuclear excellence' concept encompass beyond regulatory compliance?",
        [
            "Achieving the minimum regulatory requirements with the lowest operating costs",
            "Continuous improvement in safety, reliability, and operational performance with a goal of being the best — not just adequate — recognizing that good enough is not good enough in nuclear power",
            "Achieving maximum electricity output regardless of safety margins",
            "Compliance with all IAEA safety standards and national regulatory requirements"
        ],
        correct_index=1,
        explanation="WANO's nuclear excellence philosophy goes beyond regulatory compliance to pursue continuous improvement toward world-class performance. The concept reflects the recognition that nuclear power requires the highest standards — 'nuclear excellence' means always striving to improve, learning from others, sharing experiences openly, and rejecting complacency. It reflects the nuclear industry's acceptance that its social license depends on consistently outstanding performance.",
        difficulty=1,
        source="WANO Charter; INPO Principles"
    )

    add_question(db, wano_id,
        "What is a WANO Corporate Peer Review (CPR)?",
        [
            "A financial review of a nuclear utility's corporate governance",
            "A peer review of the corporate or fleet-level organizations that support nuclear plant operations, assessing leadership, oversight, and support functions",
            "A review of a nuclear plant's public communications and stakeholder engagement",
            "An assessment of a nuclear company's environmental performance"
        ],
        correct_index=1,
        explanation="A WANO Corporate Peer Review (CPR) assesses the corporate or fleet-level organization that supports nuclear operations — including executive leadership, nuclear oversight, engineering support, and fleet-level programs. Unlike a plant-level peer review, the CPR focuses on how the corporate organization influences and supports excellence at the plant level, recognizing that strong corporate leadership and oversight are essential for sustained nuclear performance.",
        difficulty=2,
        source="WANO Peer Review Guidelines"
    )

    add_question(db, wano_id,
        "What is INPO's 'Principles for a Strong Nuclear Safety Culture' document and what are its key attributes?",
        [
            "A legally binding regulatory document issued jointly by INPO and the NRC",
            "An INPO publication outlining ten safety culture traits including leadership, conservative decision-making, questioning attitude, and continuous learning that characterize excellent nuclear organizations",
            "A personal code of conduct for nuclear power plant operators",
            "A technical standard for nuclear plant design safety features"
        ],
        correct_index=1,
        explanation="INPO's 'Principles for a Strong Nuclear Safety Culture' (2004, updated) identifies key traits of strong nuclear safety culture: personal accountability, questioning attitude, effective safety communication, leadership commitment to safety, decision-making, respectful work environment, continuous learning, problem identification and resolution, environment for raising concerns, and work processes. These principles are widely referenced by the global nuclear industry and align with IAEA and WANO safety culture frameworks.",
        difficulty=2,
        source="INPO Safety Culture Principles"
    )

    add_question(db, wano_id,
        "How does WANO's peer review process differ from a regulatory inspection?",
        [
            "There is no meaningful difference — both assess compliance with the same standards",
            "WANO peer reviews are collaborative and advisory with no enforcement authority; regulatory inspections can result in enforcement actions and regulatory findings",
            "WANO peer reviews are more detailed than regulatory inspections",
            "Regulatory inspections are voluntary; WANO peer reviews are mandatory for all members"
        ],
        correct_index=1,
        explanation="WANO peer reviews are fundamentally different from regulatory inspections: they are conducted by peers (nuclear professionals from other plants), are collaborative and confidential in nature, identify Areas for Improvement (AFIs) rather than violations, and carry no enforcement authority. The goal is mutual improvement and learning. Regulatory inspections, by contrast, assess compliance with legal requirements and can result in violations, fines, or other enforcement actions.",
        difficulty=1,
        source="WANO Charter; IAEA Safety Standards"
    )

    add_question(db, wano_id,
        "What is the significance of the WANO 'counterfeit, fraudulent, and suspect items' (CFSI) program?",
        [
            "A program to prevent counterfeit WANO documents from being used in regulatory submissions",
            "A program to identify and prevent the use of substandard or counterfeit equipment and components in nuclear power plants that could compromise safety or reliability",
            "An anti-corruption program targeting suppliers to nuclear utilities",
            "A cybersecurity program targeting fraudulent software in plant control systems"
        ],
        correct_index=1,
        explanation="Counterfeit, fraudulent, and suspect items (CFSI) in nuclear supply chains pose serious safety risks — substandard components may fail when needed. WANO and INPO share information about identified CFSI events across the global fleet to prevent affected components from remaining in service at other plants. Strong procurement quality assurance programs are a key defense against CFSI.",
        difficulty=2,
        source="WANO Operational Experience; INPO CFSI Program"
    )

    add_question(db, wano_id,
        "What is the role of nuclear industry self-assessment in the WANO/INPO model?",
        [
            "Self-assessment is discouraged because organizations cannot objectively evaluate themselves",
            "Rigorous self-assessment is a cornerstone of the excellence model — organizations are expected to critically evaluate their own performance and identify improvements before external reviews find them",
            "Self-assessment is only required when WANO requests it prior to a peer review",
            "Self-assessment replaces external peer reviews for well-performing plants"
        ],
        correct_index=1,
        explanation="Effective self-assessment is a core element of the WANO/INPO nuclear excellence model. High-performing organizations are expected to identify weaknesses and improvement opportunities through their own rigorous self-assessment processes rather than waiting for external peer reviews to find them. A strong self-assessment program — including management observations, department self-assessments, and benchmarking — is a leading indicator of organizational health.",
        difficulty=2,
        source="WANO Self-Assessment Guidelines; INPO Good Practices"
    )

    add_question(db, wano_id,
        "What is the WANO Systematic Approach to Training (SAT) support and why is it important internationally?",
        [
            "WANO provides funding for training simulators at nuclear plants in developing countries",
            "WANO supports implementation of SAT-based training programs at member organizations globally, which is especially important for countries new to nuclear power who lack established training expertise",
            "WANO operates a central training facility where all international nuclear operators are trained",
            "WANO's SAT support only applies to WANO staff; plant operator training is a national responsibility"
        ],
        correct_index=1,
        explanation="WANO actively supports member organizations — particularly in countries newer to nuclear power — in implementing Systematic Approach to Training (SAT) based programs. This is critical because operator and maintenance training quality directly affects plant safety. For countries like the UAE, Bangladesh, or Turkey that are building their first nuclear plants, WANO SAT support helps establish competency-based training programs from the outset.",
        difficulty=2,
        source="WANO Training Support Program"
    )

    add_question(db, wano_id,
        "Following the Fukushima accident, what special actions did WANO take and what was the 'Fukushima Response Team'?",
        [
            "WANO took no specific action as Fukushima was a regulatory matter, not an industry one",
            "WANO rapidly deployed a support team to assist TEPCO and subsequently developed enhanced peer review processes focused on beyond-design-basis event preparedness",
            "WANO suspended all peer reviews pending a global safety review",
            "WANO transferred management of Japanese nuclear plants to international operators"
        ],
        correct_index=1,
        explanation="Following Fukushima, WANO played an active role: deploying support missions to assist TEPCO, issuing special communications to all member operators, and subsequently enhancing its peer review program to specifically assess beyond-design-basis event preparedness, severe accident management guidelines (SAMGs), and FLEX equipment provisions. WANO also worked with INPO on enhanced peer review criteria that became standard globally.",
        difficulty=2,
        source="WANO Post-Fukushima Response; WANO Annual Report 2011"
    )

    add_question(db, wano_id,
        "What is the 'nuclear industry's social license' and how do WANO and INPO contribute to maintaining it?",
        [
            "A formal government permit required to operate a nuclear power plant",
            "The public's implicit acceptance of nuclear power operations, which depends on demonstrated safety and excellence; WANO and INPO help maintain this by driving continuous improvement in safety performance",
            "A WANO certification that allows nuclear plants to operate internationally",
            "The financial license granted by banks for nuclear power plant construction financing"
        ],
        correct_index=1,
        explanation="The nuclear industry's 'social license' is the implicit public acceptance of nuclear power operations — not a legal permit but the public's ongoing willingness to accept nuclear plants in their communities. This depends fundamentally on demonstrated safety and operational excellence. WANO and INPO contribute by driving continuous improvement in safety performance, sharing operational experience, and holding operators accountable to the highest standards, all of which support public confidence in nuclear power.",
        difficulty=2,
        source="WANO Charter; Nuclear Industry Principles"
    )

    add_question(db, wano_id,
        "What is INPO's 'Owner's Group' concept and how does it benefit nuclear safety?",
        [
            "A legal ownership structure for nuclear power plants recommended by INPO",
            "Groups of utilities operating the same reactor type that share technical information, address common issues, and develop common solutions — supported and facilitated by INPO",
            "A shareholder group that provides financial oversight of nuclear utility operations",
            "An INPO program that transfers ownership of underperforming plants to better operators"
        ],
        correct_index=1,
        explanation="INPO facilitates Owners Groups — associations of utilities operating the same reactor type (e.g., PWR Owners Group, BWR Owners Group, CANDU Owners Group in Canada). These groups share technical information, collectively address design or operational issues, develop common solutions (like improved procedures or hardware modifications), and pool resources for technical analyses. This prevents individual utilities from having to independently resolve common technical challenges.",
        difficulty=2,
        source="INPO; CANDU Owners Group"
    )

    db.commit()
    db.close()

    print("Expansion complete!")
    print()
    print("Updated question counts (20 per existing category):")
    print("  CANDU Reactor Systems:         +7  → 20 questions")
    print("  CNSC Regulatory Framework:     +10 → 20 questions")
    print("  IAEA Safety Standards:         +11 → 20 questions")
    print("  Radiation Protection:          +11 → 20 questions")
    print("  Nuclear Security & Safeguards: +10 → 20 questions")
    print()
    print("New categories added (20 questions each):")
    print("  PWR Reactor Systems:           20 questions")
    print("  BWR Reactor Systems:           20 questions")
    print("  INPO and WANO:                 20 questions")
    print()
    print("Grand total: 160 questions across 8 categories")


if __name__ == "__main__":
    main()