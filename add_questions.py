"""
add_questions.py
Run to add additional questions to the existing database.
Usage: python add_questions.py
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


def main():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")

    # ── CANDU REACTOR SYSTEMS (category_id = 1) ──────────────────────────────

    add_question(db, 1,
        "What is the purpose of the annular space between a CANDU pressure tube and its surrounding calandria tube?",
        [
            "It carries heavy water coolant to the fuel",
            "It is filled with CO₂ or dry nitrogen and acts as a thermal barrier between hot coolant and cold moderator",
            "It houses neutron absorbing material for reactivity control",
            "It carries light water for emergency cooling"
        ],
        correct_index=1,
        explanation="The annular gap between the pressure tube and calandria tube is filled with insulating gas (CO₂ or dry N₂). This prevents heat transfer from the hot pressurized coolant (~300°C) to the cold moderator (~70°C), improving thermal efficiency and protecting the calandria tube.",
        difficulty=2,
        source="IAEA-TECDOC-1698"
    )

    add_question(db, 1,
        "What reactor physics property of CANDU reactors requires careful design attention due to the use of heavy water moderator?",
        [
            "A positive coolant void reactivity coefficient under certain conditions",
            "A strongly negative moderator temperature coefficient",
            "An inability to sustain criticality with natural uranium",
            "Excessive prompt neutron lifetime leading to instability"
        ],
        correct_index=0,
        explanation="CANDU reactors can exhibit a positive coolant void reactivity (CVR) — if coolant is lost from the fuel channels, reactivity can increase rather than decrease. This is a key safety consideration addressed through the two independent fast shutdown systems (SDS1 and SDS2).",
        difficulty=3,
        source="CNSC REGDOC-2.4.2"
    )

    add_question(db, 1,
        "In a CANDU reactor, what is the role of adjuster rods?",
        [
            "They provide emergency shutdown capability",
            "They flatten the neutron flux distribution across the core and provide bulk reactivity control",
            "They measure neutron flux for instrumentation purposes",
            "They inject poison into the moderator during a LOCA"
        ],
        correct_index=1,
        explanation="Adjuster rods are normally fully inserted into the CANDU core. They flatten the radial and axial neutron flux distribution to maximize fuel burnup uniformity. They can also be withdrawn to compensate for xenon poisoning following a reactor stepback.",
        difficulty=2,
        source="IAEA-TECDOC-1391"
    )

    add_question(db, 1,
        "What is xenon-135 and why is it significant in CANDU reactor operation?",
        [
            "A fission product with a very large neutron absorption cross-section that can suppress reactor power",
            "A moderator contaminant that reduces reactivity by absorbing thermal neutrons",
            "A radioactive gas released during fuel failures that must be monitored",
            "A corrosion product in the primary heat transport system"
        ],
        correct_index=0,
        explanation="Xenon-135 is a fission product with one of the largest thermal neutron absorption cross-sections of any nuclide. It builds up during reactor operation and decays during shutdown. Following a reactor trip, xenon buildup can prevent restart for 15-30 hours — the 'xenon precluded startup' period. CANDU operators must manage xenon transients carefully.",
        difficulty=2,
        source="IAEA Nuclear Reactor Theory"
    )

    add_question(db, 1,
        "What fuelling machine configuration is used in CANDU reactors and what does it enable?",
        [
            "A single fuelling machine that operates during scheduled outages only",
            "Two fuelling machines working from opposite ends of a fuel channel simultaneously, enabling on-power refuelling",
            "A robotic arm system that replaces entire fuel assemblies during planned maintenance",
            "A gravity-fed fuel loading system that operates during low-power operation only"
        ],
        correct_index=1,
        explanation="CANDU uses two fuelling machines that dock at opposite ends of a fuel channel simultaneously — one pushes new fuel bundles in while the other receives spent bundles. This enables refuelling at full power, eliminating the costly outages required by other reactor types for refuelling.",
        difficulty=1,
        source="IAEA-TECDOC-1391"
    )

    add_question(db, 1,
        "What is the Emergency Core Cooling System (ECCS) in a CANDU plant designed to do?",
        [
            "Cool the steam generators following a secondary side pipe break",
            "Inject water into fuel channels to remove decay heat following a Loss of Coolant Accident",
            "Provide backup cooling to the moderator system during normal operations",
            "Supply makeup water to the spent fuel bay"
        ],
        correct_index=1,
        explanation="Following a LOCA, the ECCS provides high-pressure injection of light water into the reactor headers to cool the fuel. It then transitions to a long-term recirculation mode using water collected in the reactor building to maintain fuel cooling indefinitely.",
        difficulty=1,
        source="CNSC REGDOC-2.4.2"
    )

    add_question(db, 1,
        "What is the moderator's secondary safety role in a CANDU reactor beyond neutron thermalization?",
        [
            "It acts as a backup heat sink that can absorb decay heat from the fuel in certain accident scenarios",
            "It provides emergency makeup water to the primary heat transport system",
            "It dilutes radioactive releases during a fuel failure event",
            "It moderates the response of the shutdown systems during a reactor trip"
        ],
        correct_index=0,
        explanation="In CANDU reactors, the large volume of cold heavy water moderator acts as a passive heat sink. In certain severe accident scenarios — such as a LOCA with loss of ECCS — the moderator can absorb decay heat through the calandria tubes, preventing fuel damage. This is a unique passive safety feature of the CANDU design.",
        difficulty=3,
        source="IAEA-TECDOC-1600"
    )

    add_question(db, 1,
        "What does CANDU stand for?",
        [
            "Canadian Deuterium Uranium",
            "Canadian Design Nuclear Utility",
            "CANDU Advanced Nuclear Design Unit",
            "Canadian Deuterium Universal"
        ],
        correct_index=0,
        explanation="CANDU stands for CANada Deuterium Uranium — reflecting its three key characteristics: developed in Canada, using heavy water (deuterium oxide) as moderator and coolant, and fuelled with natural uranium.",
        difficulty=1,
        source="Atomic Energy of Canada Limited"
    )

    # ── CNSC REGULATORY FRAMEWORK (category_id = 2) ──────────────────────────

    add_question(db, 2,
        "What is the name of the Canadian legislation that establishes the CNSC and its regulatory authority?",
        [
            "The Atomic Energy Act",
            "The Nuclear Safety and Control Act (NSCA)",
            "The Canadian Nuclear Regulatory Act",
            "The Radiation Protection and Nuclear Safety Act"
        ],
        correct_index=1,
        explanation="The Nuclear Safety and Control Act (NSCA), S.C. 1997, c. 9, establishes the Canadian Nuclear Safety Commission (CNSC) as Canada's nuclear regulator. It replaced the Atomic Energy Control Act and came into force in 2000.",
        difficulty=1,
        source="Nuclear Safety and Control Act, S.C. 1997, c. 9"
    )

    add_question(db, 2,
        "Under the CNSC regulatory framework, what is a Class IA nuclear facility?",
        [
            "A uranium mine or mill",
            "A nuclear power plant or prototype reactor",
            "A research laboratory handling nuclear substances",
            "A facility for processing nuclear waste"
        ],
        correct_index=1,
        explanation="Under the Class I Nuclear Facilities Regulations, a Class IA facility includes nuclear power plants, prototype power reactors, and demonstration power reactors. Class IB facilities include research reactors and critical assemblies. The distinction determines which regulations apply.",
        difficulty=2,
        source="Class I Nuclear Facilities Regulations, SOR/2000-204"
    )

    add_question(db, 2,
        "What are the 14 Safety and Control Areas (SCAs) used by CNSC to organize its regulatory framework?",
        [
            "A classification system for nuclear accidents based on severity",
            "A framework of topic areas used to assess licensee performance and organize regulatory requirements",
            "The 14 articles of the Nuclear Safety and Control Act",
            "A set of international standards adopted from IAEA safety guides"
        ],
        correct_index=1,
        explanation="The CNSC uses 14 Safety and Control Areas (SCAs) as a framework to organize regulatory requirements and assess licensee performance. They include areas such as Management System, Human Performance, Operating Performance, Safety Analysis, Physical Design, Radiation Protection, and Emergency Management among others.",
        difficulty=2,
        source="CNSC Regulatory Framework"
    )

    add_question(db, 2,
        "What is the purpose of a CNSC-required Probabilistic Safety Assessment (PSA) for nuclear power plants?",
        [
            "To determine the maximum credible accident for evacuation planning",
            "To provide a systematic quantitative assessment of risks from plant failures and their potential consequences",
            "To replace deterministic safety analysis for licence applications",
            "To assess the probability of operator errors during normal operations"
        ],
        correct_index=1,
        explanation="A Probabilistic Safety Assessment (PSA) is a systematic, quantitative method for evaluating the risk of a nuclear power plant. It identifies accident sequences, estimates their frequencies, and assesses potential consequences. CNSC requires PSA as a complement to deterministic safety analysis — not as a replacement.",
        difficulty=3,
        source="CNSC REGDOC-2.4.2"
    )

    add_question(db, 2,
        "What does the CNSC REGDOC-2.7.1 cover?",
        [
            "Physical security requirements for nuclear facilities",
            "Radiation protection requirements including dose limits, ALARA, and monitoring programs",
            "Requirements for nuclear criticality safety",
            "Environmental protection and assessment requirements"
        ],
        correct_index=1,
        explanation="CNSC REGDOC-2.7.1 sets out requirements and guidance for radiation protection programs at licensed facilities. It covers dose limits for workers and the public, the ALARA principle, radiation monitoring, dosimetry, and reporting of radiological incidents.",
        difficulty=2,
        source="CNSC REGDOC-2.7.1"
    )

    add_question(db, 2,
        "What is the role of the Canadian Nuclear Safety Commission's Secretariat in the public hearing process?",
        [
            "It makes final licensing decisions on behalf of the Commission",
            "It coordinates hearing logistics, manages interventions, and ensures the public record is complete",
            "It conducts independent technical reviews of licensee safety cases",
            "It enforces licence conditions and issues penalties for non-compliance"
        ],
        correct_index=1,
        explanation="The CNSC Secretariat supports the Commission by coordinating the public hearing process — managing the submission of interventions, scheduling hearings, maintaining the public record, and ensuring procedural fairness. The Commission Members make the actual licensing decisions.",
        difficulty=2,
        source="CNSC Rules of Procedure"
    )

    add_question(db, 2,
        "What is the significance of the Derived Release Limits (DRLs) in Canadian nuclear regulation?",
        [
            "They define the maximum radiation dose a nuclear energy worker may receive annually",
            "They are facility-specific limits on radioactive releases to the environment derived from public dose limits",
            "They set the threshold for mandatory evacuation of the public around a nuclear facility",
            "They define the maximum inventory of radioactive material permitted in a nuclear facility"
        ],
        correct_index=1,
        explanation="Derived Release Limits (DRLs) are facility-specific annual limits on the release of radionuclides to the environment. They are derived by working backward from the public dose limit (1 mSv/year) through environmental dispersion models to determine what releases are acceptable at a given site.",
        difficulty=3,
        source="CNSC REGDOC-2.9.1"
    )

    # ── IAEA SAFETY STANDARDS (category_id = 3) ──────────────────────────────

    add_question(db, 3,
        "What is the IAEA Operational Safety Review Team (OSART) mission?",
        [
            "A mandatory inspection program for all nuclear power plants in IAEA member states",
            "A peer review of operational safety practices at nuclear power plants against IAEA safety standards, conducted at the host country's request",
            "An emergency response team deployed following nuclear accidents",
            "A financial audit of nuclear power plant operating costs"
        ],
        correct_index=1,
        explanation="An OSART mission is a voluntary peer review of operational safety at a nuclear power plant requested by the plant's operating organization and/or government. International experts compare plant practices against IAEA Safety Standards and share good practices. They are not inspections — findings are recommendations, not regulatory requirements.",
        difficulty=2,
        source="IAEA Safety Standards Series No. SSG-18"
    )

    add_question(db, 3,
        "What is the Integrated Regulatory Review Service (IRRS)?",
        [
            "An IAEA peer review of a country's nuclear regulatory infrastructure against IAEA safety standards",
            "A financial review of a country's nuclear energy program",
            "An inspection of nuclear power plants by IAEA inspectors",
            "A review of a country's emergency preparedness arrangements"
        ],
        correct_index=0,
        explanation="The IRRS is a voluntary, comprehensive peer review service offered by the IAEA to assess a country's regulatory framework for nuclear, radiation, radioactive waste, and transport safety against IAEA Safety Standards. Canada has hosted IRRS missions and uses findings to strengthen the CNSC's regulatory framework.",
        difficulty=2,
        source="IAEA Safety Standards Series No. GSR Part 1"
    )

    add_question(db, 3,
        "According to IAEA GSR Part 3, what is the occupational effective dose limit for workers?",
        [
            "20 mSv per year averaged over 5 years, with no more than 50 mSv in any single year",
            "50 mSv per year with no multi-year averaging",
            "100 mSv per year for nuclear power plant workers",
            "20 mSv per year as an absolute annual limit"
        ],
        correct_index=0,
        explanation="IAEA GSR Part 3 sets the occupational effective dose limit at 20 mSv per year averaged over 5 consecutive years (100 mSv in 5 years), with the additional constraint that no more than 50 mSv may be received in any single year. This aligns with ICRP Publication 103 recommendations.",
        difficulty=2,
        source="IAEA GSR Part 3, Requirement 13"
    )

    add_question(db, 3,
        "What is the IAEA's definition of 'Defence in Depth' as it applies to nuclear installations?",
        [
            "The physical depth of containment structures surrounding a reactor",
            "A hierarchical deployment of multiple independent levels of protection so that a single failure does not lead to harmful consequences",
            "The number of security barriers protecting nuclear material from theft",
            "The depth of the exclusion zone around a nuclear power plant"
        ],
        correct_index=1,
        explanation="Defence in depth is a safety philosophy requiring multiple independent levels of protection — physical barriers, safety systems, and procedural controls — such that no single failure leads to radiological harm. It ensures that if one level fails, the next level provides protection. This concept is central to all IAEA nuclear safety standards.",
        difficulty=1,
        source="IAEA SF-1, INSAG-10"
    )

    add_question(db, 3,
        "What does the IAEA Nuclear Safety Action Plan, adopted after Fukushima, primarily address?",
        [
            "New financial mechanisms for nuclear power plant construction in developing countries",
            "Strengthening nuclear safety worldwide through targeted actions in areas exposed as weaknesses by the Fukushima accident",
            "International sanctions against countries that fail to meet IAEA safety standards",
            "Mandatory phase-out of boiling water reactor technology globally"
        ],
        correct_index=1,
        explanation="Following the 2011 Fukushima Daiichi accident, IAEA member states adopted a Nuclear Safety Action Plan in September 2011. It identifies 12 areas for strengthening nuclear safety globally, including stress tests, emergency preparedness, national regulatory frameworks, and IAEA peer reviews.",
        difficulty=2,
        source="IAEA Nuclear Safety Action Plan (2011)"
    )

    add_question(db, 3,
        "In IAEA terminology, what is the difference between a 'safety requirement' and a 'safety guide'?",
        [
            "Safety requirements are voluntary while safety guides are mandatory",
            "Safety requirements state what must be done; safety guides recommend how to meet the requirements",
            "Safety requirements apply to reactor safety; safety guides apply to radiation protection",
            "There is no practical difference — both carry equal regulatory weight"
        ],
        correct_index=1,
        explanation="In the IAEA Safety Standards Series, Safety Requirements (GSR/SSR) use the language 'shall' to define what must be accomplished. Safety Guides (GSG/SSG) use 'should' to recommend means of meeting requirements. Guides are not mandatory — alternatives may be used if they achieve equivalent safety.",
        difficulty=1,
        source="IAEA SF-1"
    )

    # ── RADIATION PROTECTION (category_id = 4) ──────────────────────────────

    add_question(db, 4,
        "What is the difference between absorbed dose and effective dose?",
        [
            "Absorbed dose measures radiation energy deposited per unit mass; effective dose applies tissue and radiation weighting factors to reflect biological risk",
            "Absorbed dose applies to workers; effective dose applies to the general public",
            "Absorbed dose is measured externally; effective dose is measured internally",
            "There is no difference — the terms are used interchangeably"
        ],
        correct_index=0,
        explanation="Absorbed dose (measured in Gray, Gy) is the energy deposited by radiation per kilogram of tissue. Effective dose (measured in Sievert, Sv) applies radiation weighting factors (wR) for different radiation types and tissue weighting factors (wT) for different organs, giving a single measure of overall biological detriment.",
        difficulty=2,
        source="ICRP Publication 103; CNSC REGDOC-2.7.1"
    )

    add_question(db, 4,
        "What are the three fundamental methods of reducing external radiation dose?",
        [
            "Shielding, dilution, and containment",
            "Time, distance, and shielding",
            "Monitoring, ventilation, and personal protective equipment",
            "Decontamination, evacuation, and iodine prophylaxis"
        ],
        correct_index=1,
        explanation="The three fundamental principles of external radiation protection are: Time (minimize time spent near a source), Distance (maximize distance from the source — dose rate follows the inverse square law), and Shielding (place absorbing material between the source and personnel).",
        difficulty=1,
        source="IAEA GSR Part 3; CNSC REGDOC-2.7.1"
    )

    add_question(db, 4,
        "What is a Committed Effective Dose and when is it used?",
        [
            "The dose committed to workers at the start of a maintenance outage",
            "The total effective dose that will result over 50 years (adults) from an internal radionuclide intake",
            "The maximum dose permitted in a single emergency intervention",
            "The dose limit committed to in a licensee's radiation protection program"
        ],
        correct_index=1,
        explanation="Committed Effective Dose (CED) accounts for internal radiation from radionuclide intakes. It integrates the dose delivered over 50 years for adults (or 70 years for children) following a single intake. It is attributed to the year of intake regardless of when the dose is actually delivered to tissues.",
        difficulty=3,
        source="ICRP Publication 103"
    )

    add_question(db, 4,
        "What is the annual effective dose limit for members of the public from licensed nuclear activities in Canada?",
        [
            "5 mSv/year",
            "1 mSv/year",
            "0.1 mSv/year",
            "20 mSv/year"
        ],
        correct_index=1,
        explanation="The Radiation Protection Regulations limit the effective dose to members of the public from licensed nuclear activities to 1 mSv per year. This is in addition to natural background radiation and medical exposures. It aligns with the ICRP and IAEA recommended public dose limit.",
        difficulty=1,
        source="Radiation Protection Regulations, SOR/2000-203, Section 13"
    )

    add_question(db, 4,
        "What is the purpose of a Nuclear Energy Worker (NEW) designation under Canadian regulations?",
        [
            "It entitles the worker to higher pay due to radiation exposure",
            "It subjects the worker to higher dose limits and requires dosimetry, training, and medical surveillance",
            "It restricts the worker from entering high radiation areas without supervision",
            "It certifies the worker as qualified to handle radioactive sources"
        ],
        correct_index=1,
        explanation="A Nuclear Energy Worker (NEW) is a person who is required, in the course of their work, to receive a dose greater than the public dose limit. NEWs are subject to the higher occupational dose limits (50 mSv/year, 100 mSv/5 years), individual dosimetry requirements, radiation safety training, and biological monitoring where required.",
        difficulty=2,
        source="Radiation Protection Regulations, SOR/2000-203"
    )

    add_question(db, 4,
        "What type of radiation is most effectively shielded by high-density materials such as lead?",
        [
            "Alpha particles",
            "Beta particles",
            "Gamma rays and X-rays",
            "Neutrons"
        ],
        correct_index=2,
        explanation="Gamma rays and X-rays are high-energy electromagnetic radiation that require dense, high-atomic-number materials like lead or thick concrete for effective shielding. Alpha particles are stopped by a sheet of paper or skin. Beta particles are shielded by plastic or aluminum. Neutrons require hydrogen-rich materials like water or polyethylene.",
        difficulty=1,
        source="IAEA Basic Radiation Physics"
    )

    add_question(db, 4,
        "What is the inverse square law and how does it apply to radiation protection?",
        [
            "Dose rate decreases by half for each half-life of the radionuclide",
            "Dose rate decreases proportionally to the square of the distance from the source",
            "Shielding effectiveness doubles with each doubling of shield thickness",
            "Dose rate increases with the square of the radiation energy"
        ],
        correct_index=1,
        explanation="The inverse square law states that radiation intensity (dose rate) decreases proportionally to the square of the distance from a point source. Doubling your distance from a source reduces the dose rate to one quarter. For example, moving from 1m to 2m reduces dose rate by a factor of 4. This makes distance one of the most effective radiation protection tools.",
        difficulty=1,
        source="IAEA Basic Radiation Physics"
    )

    # ── NUCLEAR SECURITY & SAFEGUARDS (category_id = 5) ──────────────────────

    add_question(db, 5,
        "What are the three pillars of the IAEA safeguards system?",
        [
            "Inspections, sanctions, and reporting",
            "Nuclear material accountancy, containment, and surveillance",
            "Physical protection, transport security, and border monitoring",
            "State declarations, facility design, and export controls"
        ],
        correct_index=1,
        explanation="IAEA safeguards rest on three pillars: (1) Nuclear Material Accountancy — tracking all nuclear material through measurement and records; (2) Containment — using seals and other measures to detect unauthorized access; and (3) Surveillance — using cameras and other monitoring to detect undeclared activities.",
        difficulty=2,
        source="IAEA INFCIRC/153"
    )

    add_question(db, 5,
        "What is a Significant Quantity (SQ) in IAEA safeguards terminology?",
        [
            "The minimum amount of nuclear material that could potentially be used to make a nuclear explosive device",
            "The maximum amount of nuclear material that can be stored at a facility without special measures",
            "The quantity of nuclear material that triggers mandatory reporting to the IAEA",
            "The amount of nuclear material produced annually by a typical power reactor"
        ],
        correct_index=0,
        explanation="A Significant Quantity (SQ) is the approximate amount of nuclear material for which the possibility of manufacturing a nuclear explosive device cannot be excluded. For example, 8 kg of plutonium or 25 kg of highly enriched uranium constitute one SQ. Safeguards aim to detect the diversion of even one SQ.",
        difficulty=3,
        source="IAEA Safeguards Glossary"
    )

    add_question(db, 5,
        "What is the Non-Proliferation Treaty (NPT) and what are its three pillars?",
        [
            "A bilateral treaty between the US and Russia; disarmament, verification, and compliance",
            "A multilateral treaty; non-proliferation, disarmament, and peaceful use of nuclear energy",
            "An IAEA resolution; safeguards, physical protection, and export controls",
            "A UN Security Council resolution; sanctions, inspections, and treaty compliance"
        ],
        correct_index=1,
        explanation="The Treaty on the Non-Proliferation of Nuclear Weapons (NPT), in force since 1970, has three pillars: (1) Non-proliferation — non-nuclear weapon states agree not to acquire nuclear weapons; (2) Disarmament — nuclear weapon states commit to disarmament; (3) Peaceful use — all states may develop nuclear energy for peaceful purposes.",
        difficulty=2,
        source="Treaty on the Non-Proliferation of Nuclear Weapons (1968)"
    )

    add_question(db, 5,
        "What is INFCIRC/225 and what does it cover?",
        [
            "The model Comprehensive Safeguards Agreement for NPT states",
            "The IAEA recommendations on physical protection of nuclear material and nuclear facilities",
            "The Additional Protocol requiring expanded state declarations",
            "The IAEA convention on nuclear safety"
        ],
        correct_index=1,
        explanation="IAEA INFCIRC/225 (currently Rev. 5) contains IAEA recommendations on the physical protection of nuclear material and nuclear facilities. It defines protection levels for different categories of nuclear material and sets requirements for physical protection systems including detection, delay, and response.",
        difficulty=2,
        source="IAEA INFCIRC/225/Rev.5"
    )

    add_question(db, 5,
        "What is Canada's role in the Nuclear Suppliers Group (NSG)?",
        [
            "Canada is not a member of the NSG",
            "Canada is a founding member and applies NSG guidelines to control exports of nuclear-related materials and technology",
            "Canada chairs the NSG as the world's largest uranium producer",
            "Canada participates as an observer but does not apply NSG export controls"
        ],
        correct_index=1,
        explanation="Canada is a founding member of the Nuclear Suppliers Group (NSG), established in 1975. The NSG is a multilateral export control regime whose members apply common guidelines to control exports of nuclear materials, equipment, and technology to prevent their use in nuclear weapons programs. As a major uranium and CANDU technology exporter, Canada's NSG membership is significant.",
        difficulty=2,
        source="Nuclear Suppliers Group; Global Affairs Canada"
    )

    add_question(db, 5,
        "What is the Convention on Nuclear Safety (CNS) and what does it require of signatories?",
        [
            "A mandatory treaty requiring all states to shut down older nuclear power plants",
            "A legally binding international instrument requiring states to report on the safety of their civil nuclear power plants at periodic review meetings",
            "An IAEA convention establishing mandatory safety standards for all member states",
            "A bilateral agreement between nuclear weapon states on reactor safety"
        ],
        correct_index=1,
        explanation="The Convention on Nuclear Safety (CNS), in force since 1996, is an incentive instrument requiring signatory states to submit national reports on the safety of their land-based civil nuclear power plants. These reports are peer reviewed at triennial Review Meetings. Canada is a signatory and submits regular reports covering all operating CANDU plants.",
        difficulty=2,
        source="Convention on Nuclear Safety, IAEA INFCIRC/449"
    )

    add_question(db, 5,
        "What is the purpose of the State System of Accounting for and Control of Nuclear Material (SSAC)?",
        [
            "To manage the financial accounts of a state's nuclear energy program",
            "To provide the national infrastructure for tracking nuclear material that supports IAEA safeguards verification",
            "To control exports of nuclear material to non-NPT states",
            "To manage radioactive waste accounting at nuclear facilities"
        ],
        correct_index=1,
        explanation="A State System of Accounting for and Control (SSAC) is the national nuclear material accountancy system that each state is required to establish under its safeguards agreement. It provides the infrastructure — records, reports, and measurement systems — that the IAEA uses to verify that no nuclear material has been diverted. In Canada, the CNSC operates the SSAC.",
        difficulty=3,
        source="IAEA INFCIRC/153; CNSC Regulatory Framework"
    )

    db.commit()
    db.close()

    print("Done! Added questions:")
    print("  CANDU Reactor Systems:        8 new questions")
    print("  CNSC Regulatory Framework:    7 new questions")
    print("  IAEA Safety Standards:        6 new questions")
    print("  Radiation Protection:         7 new questions")
    print("  Nuclear Security & Safeguards:7 new questions")
    print("  Total: 35 new questions added")


if __name__ == "__main__":
    main()