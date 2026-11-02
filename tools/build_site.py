"""Build the multi-page EN/BG site into website/.

Rename the firm by editing BRAND / DOMAIN below and re-running:
    python tools/build_site.py
Name-specific story copy lives in the `about_name_*` strings in the dictionary.
"""
import html as _html
import json
import os
import re
from pathlib import Path

BRAND = "Pistiros Advisory"
DOMAIN = "pistiros.com"             # to register
EMAIL = "pistirosadvisory@gmail.com"   # placeholder until the domain mailbox exists
SHOW_BIO = False   # hide principal bio + photo until the lawyer questions are resolved
SHOW_DOWNLOADS = False  # sample PDFs: hide until lawyer has seen them
PREVIEW = False    # True = noindex on every page (feedback phase); False = visible to search engines
NOINDEX = '<meta name="robots" content="noindex, nofollow">' if PREVIEW else ""
# live address used for canonical URLs, Open Graph and sitemap.xml; change when the domain is bought
SITE_URL = "https://pistirosadvisory.github.io/pistiros-advisory/"
# paste the content="..." value from Google Search Console / Bing Webmaster Tools (HTML meta-tag method)
GOOGLE_VERIFY = "CxgrujzgHvp-TiK4QchWLrI8DmUKiuZQQ7jb8icF-f8"
BING_VERIFY = ""

ROOT = Path(__file__).resolve().parent.parent
OUT = Path(os.environ.get("PISTIROS_SITE_OUT", str(ROOT)))
INSIGHTS_SRC = ROOT / "content" / "insights"
# Insights categories, in page order; each article's "Category:" line holds one of these keys.
# Source files are picked up automatically; "NN-insight-" filename prefixes only set the order.
CATEGORIES = ["outlook", "guides", "risk", "regulatory", "sectors", "regional"]

# --------------------------------------------------------------------------- dictionary
EN = {
 "nav_services": "Services", "nav_clients": "Clients", "nav_principles": "Principles", "nav_insights": "Insights", "nav_about": "About", "nav_contact": "Contact",
 "title_home": "{B} — The compliant gateway between the EU and the East",
 "title_services": "Services — {B}", "title_clients": "Clients — {B}", "title_principles": "Principles — {B}", "title_insights": "Insights — {B}", "title_about": "About — {B}",

 # home
 "h_eyebrow": "Management consulting · Bulgaria",
 "h_h1": "The compliant gateway between the EU and the East.",
 "h_lead": "Independent supplier verification and sanctions readiness for companies trading across the EU's south-eastern frontier. Fixed fees. No access brokering.",
 "h_cta1": "Our services", "h_cta2": "Get in touch",
 "why_eyebrow": "Why it matters", "why_h2": "A bridge only carries traffic if both ends trust it.",
 "why_p1": "Bulgaria sits on the EU's land border with Turkey, on the Black Sea and the Danube, and at the western end of the Middle Corridor from Central Asia and the Caucasus. With the euro and Schengen, it is a natural entry point to the single market.",
 "why_p2": "That position is only worth what the market believes about it. Western buyers need to know who owns a supplier, where its goods end up, and whether its paperwork stands up. Companies in the region need to be able to show it. We sit between the two.",
 "hs_eyebrow": "What we do", "hs_h2": "One method, four services.",
 "hs_more": "All services →",
 "pl_eyebrow": "Principles", "pl_h2": "Independent. Not for sale.",
 "pl1_h": "Fixed fees", "pl1_p": "No success fees, no contingent payments, no payments to or through officials.",
 "pl2_h": "One side only", "pl2_p": "Never buyer and supplier on the same transaction. Every engagement is logged.",
 "pl3_h": "Lawful sources", "pl3_p": "Open sources, registries and client documents. Evidence graded, never overstated.",
 "pl_more": "Read our principles →",
 "cta_h2": "Start with an email.",
 "cta_lead": "Tell us briefly who you are and what you need checked or prepared. We reply within two working days.",

 # services
 "sv_eyebrow": "Services", "sv_h1": "One method, four services.",
 "sv_lead": "Every engagement follows the same logic: establish the facts, close the gaps, and keep the result current.",
 "m1": "Verify", "m1d": "Ownership, sanctions exposure, diversion risk and certifications, checked against lawful sources.",
 "m2": "Prepare", "m2d": "Close the gaps buyers and regulators will ask about, and document them properly.",
 "m3": "Monitor", "m3d": "Re-check on a schedule so a clean result stays clean.",
 "s1_h": "Supplier Verification", "s1_for": "For buyers",
 "s1_p": "An independent, evidence-graded check on a Bulgarian or Balkan supplier, at three depths. A Desk Check covers registry history, ownership and control, court and insolvency records, sanctions and politically exposed persons, and Bulgarian- and English-language media. A Full Assessment adds a site visit, a management interview, certificate checks with the issuers, and a review of customers, end use and payment routes. An Enhanced Assessment adds onward-route and diversion analysis. Every report ends with a red, amber or green verdict.",
 "s1_s": "Desk Check about 5 working days; Full Assessment 10–15; Enhanced 3–4 weeks. Fixed fee, agreed upfront.",
 "s2_h": "Defence Supply-Chain Evidence", "s2_for": "For defence buyers and their suppliers",
 "s2_p": "Defence programmes funded under the EU's SAFE instrument require at least 65% of component cost to come from the EU, the EEA or Ukraine, and suppliers not to be controlled from outside them. We map ownership and control to the ultimate owners, assemble the evidence on where components come from, and log licences and red flags. We prepare and test the evidence; the contracting authority decides eligibility. We act for the buyer or the supplier, never both on one programme.",
 "s2_s": "Typically 3–5 weeks per supplier.",
 "s3_h": "Sanctions Readiness", "s3_for": "For Bulgarian and Balkan exporters",
 "s3_p": "For companies selling to Turkey, the Caucasus, Central Asia and the Gulf. Bulgaria is moving to make breaching or circumventing EU sanctions a criminal offence, and banks and buyers already ask for proof of controls. We assess gaps against the European Commission's guidance on internal compliance programmes, set up counterparty screening and files for high-risk customers, train staff, and write a short policy you can show banks and customers. Contract wording is for your lawyers; we work alongside them.",
 "s3_s": "Typically 2–3 weeks. Training can be booked separately.",
 "sec_h": "Sectors we work across",
 "sec1": "Defence and dual-use", "sec2": "Automotive and industrial electronics", "sec3": "Software, AI and compute",
 "sec4": "Nuclear and grid energy", "sec5": "Logistics and Black Sea ports", "sec6": "Pharma and life sciences",
 "sec7": "Machined and fabricated metal parts", "sec8": "Financial services and fintech",
 "in_eyebrow": "Sample work", "in_h2": "Show, don't tell.",
 "in_lead": "Examples of how we work. The sample assessment describes a fictional company; it shows structure and depth, not a real client.",
 "d1_t": "Sample report", "d1_h": "Supplier Verification: Full Assessment", "d1_p": "An illustrative assessment of a fictional supplier, from executive verdict to findings register.",
 "d2_t": "Checklist", "d2_h": "What Western buyers ask Bulgarian suppliers", "d2_p": "A one-page readiness checklist covering ownership, sanctions, end-use, export controls and certification.",
 "d3_t": "Research", "d3_h": "Bulgaria as a compliant gateway", "d3_p": "An excerpt from our regional research: what changed, where the risk sits, and what buyers should watch.",
 "in_note": "Downloads are in English.",
 "sc_eyebrow": "Scope", "sc_h2": "What we are, and what we are not.",
 "sc_p": "{B} is a management consultancy. Our reports are assessments from lawful sources. They are not legal advice and not a legal classification of goods. We do not provide:",
 "sc1": "Legal advice or opinions", "sc2": "Statutory audit or assurance opinions", "sc3": "Tax or accounting services",
 "sc4": "Customs representation or licence applications", "sc5": "Financial or investment advice", "sc6": "Company formation services",
 "sc_p2": "Where formal advice is needed, we recommend independent counsel.",

 # clients
 "cl_eyebrow": "Clients", "cl_h1": "Both sides of the same transaction. Never at once.",
 "cl_lead": "We work with the parties who carry the risk, and with the companies who need to prove they are worth trusting.",
 "cl1_h": "Western buyers", "cl1_p": "Procurement, supplier-quality and compliance teams onboarding suppliers in Bulgaria and the Balkans, and the banks, insurers and sourcing agents behind them.",
 "cl1_w": "Typically: Supplier Verification, Monitoring.",
 "cl2_h": "Defence programmes", "cl2_p": "Prime contractors, integrators and their Bulgarian and Balkan suppliers on EU- and NATO-funded programmes, who need ownership and origin evidence that stands up.",
 "cl2_w": "Typically: Defence Supply-Chain Evidence.",
 "cl3_h": "Bulgarian and Balkan exporters", "cl3_p": "Manufacturers, traders and forwarders who sell east and south, or supply Western customers, and need the controls and documents that show they are a safe counterparty.",
 "cl3_w": "Typically: Sanctions Readiness, Monitoring.",
 "cl_note": "We never act for the buyer and the supplier on the same transaction. Every engagement is logged.",
 "pr_eyebrow": "Principles", "pr_h2": "Independent. Not for sale.",
 "pr_lead": "Our reports are only worth something because nobody can buy a different answer. We are not an access broker, and we do not sell introductions, influence or speed through the system.",
 "t_h1": "Access brokers", "t_h2": "{B}",
 "t_r1": "Sell", "t_a1": "Access and outcomes", "t_b1": "Assurance and readiness",
 "t_r2": "Main asset", "t_a2": "Contacts", "t_b2": "Method, evidence, independence",
 "t_r3": "Paid by", "t_a3": "Whoever wants the result", "t_b3": "The party carrying the risk",
 "t_r4": "Fees", "t_a4": "Often contingent on success", "t_b4": "Fixed. Never contingent.",
 "p1": "<b>Fixed fees only.</b> No success fees, no contingent payments, and no payments to or through officials.",
 "p2": "<b>No evasion.</b> We do not help anyone avoid export controls, sanctions or end-use checks, and we walk away from those who ask.",
 "p3": "<b>Lawful sources only.</b> Open sources, registries and client-provided documents. No covert collection.",
 "p4": "<b>Evidence, graded.</b> Every finding is marked confirmed, probable or possible, and fact is kept apart from inference.",
 "p5": "<b>Conflicts managed.</b> One side of a transaction only. Cooling-off periods and written disclosure before any later interest in a sector we have advised on.",

 # about
 "ab_eyebrow": "About", "ab_h1": "A trading post with rules.",
 "ab_lead": "{B} exists because Bulgaria's position on the EU's south-eastern edge is valuable only if the people trading across it can trust one another.",
 "an_h": "The name",
 "an_p1": "Pistiros was a trading post in the Maritsa valley, near today's Vetren in southern Bulgaria, active from the fifth century BC. Merchants from the Greek cities of Thasos, Maroneia and Apollonia traded there with the Thracians, under the protection of the Odrysian kings.",
 "an_p2": "In 1990 archaeologists found a stone there recording a royal oath to those merchants: their debts would not be cancelled, their land would not be taken from them, and their disputes would be judged among their own people. It is an early record from the Bulgarian lands of a ruler guaranteeing the rules of trade. Twenty-four centuries later the idea is the same, and it is our business: a crossing point is only as valuable as the trust and the rules it can offer.",
 "ap_h": "The problem we solve",
 "ap_p1": "Since joining the euro and Schengen, Bulgaria is a natural gateway between the EU and Turkey, the Caucasus, Central Asia and the Gulf. But a Western buyer onboarding a supplier here still struggles to tell who really owns it, where its goods end up, and whether its certificates are genuine. Capable local companies struggle the other way round: they are sound, but cannot show it in the form a Western compliance team expects.",
 "ap_p2": "The usual options do not fit. Large firms are priced for large mandates. Local fixers sell access, which is exactly what a careful buyer does not want. We fill the gap: independent, evidence-based work, for a fixed fee, for the party carrying the risk.",
 "pr_h": "Principal",
 "bio_name": "Stefan Bonchev", "bio_role": "Founder, {B}",
 "bio_p1": "Stefan has over eight years in institutional finance, accounting and operations in London, at Jefferies, PVH, Ripple and BenevolentAI, and has worked in investment operations for private family offices and in frontier finance. He holds an MA in Finance and Spanish and works in English, Bulgarian and Spanish.",
 "bio_p2": "That background is the work this firm does. Checking who owns what, whether the numbers and controls hold up, and how money actually moves are the questions a Western buyer or its bank asks of a supplier on the EU's frontier. Stefan has spent his career answering them from the operations side, where the paperwork has to be right.",

 # shared
 "cl_pr_link": "Read our principles →",
 "ins_eyebrow": "Insights", "ins_h1": "Notes on the region.",
 "ins_lead": "Market reports and regional briefings on Bulgaria, the Balkans and the routes to Turkey, the Caucasus and Central Asia, written to help buyers and companies understand the ground they are trading on.",
 "ins_empty_h": "The first pieces are in preparation.",
 "ins_empty_p": "Email us if you would like to hear when the first report is published.",
 "art_note": "This article is in English.", "art_back": "← All insights", "art_src": "Sources", "ins_list_h": "Sample pieces",
 "cat_outlook": "Outlook", "cat_guides": "Guides", "cat_risk": "Risk briefs", "cat_regulatory": "Regulatory",
 "cat_sectors": "Sector deep dives", "cat_regional": "Regional briefs",
 "catd_outlook": "Our annual view of Bulgaria as a supplier base: country and counterparty risk, a sector scorecard, corridors, key dates and scenarios.",
 "catd_guides": "Practical how-tos for checking a counterparty, reading a tender and protecting a contract.",
 "catd_risk": "Where sanctions, ownership, governance and illicit-trade risks sit, and how they reach a buyer's supply chain.",
 "catd_regulatory": "EU and Bulgarian rules that change what buyers and exporters must do: export controls, carbon, deforestation, investment screening, sanctions enforcement.",
 "catd_sectors": "Bulgarian industries one at a time: what is made, who makes it, and what to check before buying.",
 "catd_regional": "Bulgaria's neighbours and corridors, from Romania and Greece to Turkey, the Caucasus, Central Asia and Ukraine.",
 "art_corr": "Every fact in this note comes from a dated public source listed above. If you think something is wrong or out of date, email us and we will check it and correct it promptly.",
 "art_more": "More in this category", "art_outlook": "Read the Bulgarian Supplier Outlook 2026 →",
 "ct_btn": "Email us",
 "pv_sum": "Privacy",
 "pv_p": "This site has no forms, sets no cookies and runs no analytics. If you email us, we use your address and message only to reply and to carry out any work you ask for, and do not share them. The site is hosted on GitHub Pages, which may keep ordinary server logs outside our control.",
 "f1_h": "Disclaimer", "f1_p": "Content on this website is general information and does not constitute legal, tax, financial, investment or other professional advice. Reading it does not create a client relationship.",
 "f2_h": "Regulatory status", "f2_p": "{B} is a management consultancy. It is not a law firm, audit firm or tax adviser, and is not authorised or regulated by the Financial Conduct Authority or any financial regulator.",
 "f3_h": "Independence", "f3_p": "We take fixed fees only, broker no access, and do not act for both sides of a transaction.",
 "f_fine": "All rights reserved.",
 "s4_h": "Monitoring",
 "s4_for": "For existing clients",
 "s4_p": "Suppliers change owners, customers and fortunes. Every quarter we re-screen your suppliers or customers and alert you to changes in ownership, court records, sanctions status and media coverage, with an annual site visit as an option.",
 "s4_s": "Annual fixed fee per company monitored.",
}

BG = {
 "nav_services": "Услуги", "nav_clients": "Клиенти", "nav_principles": "Принципи", "nav_insights": "Анализи", "nav_about": "За нас", "nav_contact": "Контакт",
 "title_home": "{B} — Надежден и съобразен с правилата вход между ЕС и Изтока",
 "title_services": "Услуги — {B}", "title_clients": "Клиенти — {B}", "title_principles": "Принципи — {B}", "title_insights": "Анализи — {B}", "title_about": "За нас — {B}",

 "h_eyebrow": "Управленско консултиране · България",
 "h_h1": "Надежден и съобразен с правилата вход между ЕС и Изтока.",
 "h_lead": "Независима проверка на доставчици и готовност за санкционно съответствие за компании, търгуващи през югоизточната граница на ЕС. Фиксирани такси. Без посредничество за достъп.",
 "h_cta1": "Нашите услуги", "h_cta2": "Свържете се с нас",
 "why_eyebrow": "Защо е важно", "why_h2": "Мостът носи трафик само ако му вярват и от двата края.",
 "why_p1": "България е на сухопътната граница на ЕС с Турция, на Черно море и Дунав, и в западния край на Средния коридор от Централна Азия и Кавказ. С еврото и Шенген тя е естествена входна точка към единния пазар.",
 "why_p2": "Това положение струва толкова, колкото пазарът вярва в него. Западните купувачи трябва да знаят кой притежава доставчика, къде отиват стоките му и дали документите му издържат проверка. Компаниите в региона трябва да могат да го докажат. Ние сме между двете страни.",
 "hs_eyebrow": "Какво правим", "hs_h2": "Един метод, четири услуги.",
 "hs_more": "Всички услуги →",
 "pl_eyebrow": "Принципи", "pl_h2": "Независими. Не се купуваме.",
 "pl1_h": "Фиксирани такси", "pl1_p": "Без възнаграждение при успех, без условни плащания, без плащания към или чрез длъжностни лица.",
 "pl2_h": "Само една страна", "pl2_p": "Никога купувач и доставчик по една и съща сделка. Всеки ангажимент се вписва в дневник.",
 "pl3_h": "Законни източници", "pl3_p": "Отворени източници, регистри и документи на клиента. Доказателствата са градирани и не се преувеличават.",
 "pl_more": "Прочетете принципите ни →",
 "cta_h2": "Започнете с имейл.",
 "cta_lead": "Опишете накратко кои сте и какво трябва да бъде проверено или подготвено. Отговаряме в рамките на два работни дни.",

 "sv_eyebrow": "Услуги", "sv_h1": "Един метод, четири услуги.",
 "sv_lead": "Всеки ангажимент следва една логика: установяваме фактите, затваряме пропуските и поддържаме резултата актуален.",
 "m1": "Проверка", "m1d": "Собственост, санкционна експозиция, риск от отклоняване и сертификати, проверени по законни източници.",
 "m2": "Подготовка", "m2d": "Затваряне на пропуските, за които ще питат купувачите и регулаторите, и коректното им документиране.",
 "m3": "Наблюдение", "m3d": "Повторни проверки по график, за да остане чистият резултат чист.",
 "s1_h": "Проверка на доставчик", "s1_for": "За купувачи",
 "s1_p": "Независима проверка с градирани доказателства на български или балкански доставчик, в три нива. Документалната проверка обхваща историята в търговския регистър, собствеността и контрола, съдебни производства и несъстоятелност, санкции и видни политически личности, както и публикации в медиите на български и английски. Пълната оценка добавя посещение на място, разговор с ръководството, проверка на сертификатите при издателите им и преглед на клиентите, крайната употреба и платежните канали. Разширената оценка добавя анализ на последващите маршрути и риска от отклоняване. Всеки доклад завършва с оценка червено, жълто или зелено.",
 "s1_s": "Документална проверка около 5 работни дни; пълна оценка 10–15; разширена 3–4 седмици. Фиксирана такса, договорена предварително.",
 "s2_h": "Доказателства за отбранителни вериги на доставки", "s2_for": "За купувачи в отбраната и техните доставчици",
 "s2_p": "Отбранителните програми, финансирани по инструмента SAFE на ЕС, изискват поне 65% от стойността на компонентите да идва от ЕС, ЕИП или Украйна, а доставчиците да не са контролирани извън тях. Проследяваме собствеността и контрола до действителните собственици, събираме доказателствата за произхода на компонентите и описваме лицензите и рисковите сигнали. Ние подготвяме и проверяваме доказателствата; решението за допустимост е на възложителя. Работим за купувача или за доставчика, никога за двамата по една програма.",
 "s2_s": "Обикновено 3–5 седмици на доставчик.",
 "s3_h": "Готовност за санкционно съответствие", "s3_for": "За български и балкански износители",
 "s3_p": "За компании, които продават за Турция, Кавказ, Централна Азия и Персийския залив. България въвежда наказателна отговорност за нарушаване и заобикаляне на санкциите на ЕС, а банките и купувачите вече искат доказателство за контроли. Оценяваме пропуските спрямо насоките на Европейската комисия за вътрешни програми за съответствие, въвеждаме проверка на контрагенти и досиета за високорискови клиенти, обучаваме служителите и изготвяме кратка политика, която да покажете на банки и клиенти. Договорните клаузи са работа на вашите юристи; работим заедно с тях.",
 "s3_s": "Обикновено 2–3 седмици. Обучението може да се заяви отделно.",
 "sec_h": "Сектори, в които работим",
 "sec1": "Отбрана и продукти с двойна употреба", "sec2": "Автомобилна индустрия и индустриална електроника", "sec3": "Софтуер, изкуствен интелект и изчислителна мощ",
 "sec4": "Ядрена и мрежова енергетика", "sec5": "Логистика и черноморски пристанища", "sec6": "Фармация и науки за живота",
 "sec7": "Машинно обработени и метални изделия", "sec8": "Финансови услуги и финтех",
 "in_eyebrow": "Примерна работа", "in_h2": "По-добре да се покаже, отколкото да се обещае.",
 "in_lead": "Примери как работим. Примерният доклад описва измислена компания; показва структурата и дълбочината, а не реален клиент.",
 "d1_t": "Примерен доклад", "d1_h": "Проверка на доставчик: пълна оценка", "d1_p": "Илюстративна оценка на измислен доставчик, от обобщената оценка до регистъра на констатациите.",
 "d2_t": "Контролен списък", "d2_h": "Какво питат западните купувачи български доставчици", "d2_p": "Едностраничен списък за готовност: собственост, санкции, крайна употреба, експортен контрол и сертификати.",
 "d3_t": "Анализ", "d3_h": "България като надежден и съобразен с правилата вход", "d3_p": "Откъс от регионалните ни анализи: какво се промени, къде е рискът и какво да следят купувачите.",
 "in_note": "Материалите са на английски.",
 "sc_eyebrow": "Обхват", "sc_h2": "Какво сме и какво не сме.",
 "sc_p": "{B} е консултантска фирма по управление. Докладите ни са оценки по законни източници. Те не са правен съвет и не представляват правна класификация на стоки. Не предоставяме:",
 "sc1": "Правни съвети или становища", "sc2": "Задължителен одит или одиторски становища", "sc3": "Данъчни или счетоводни услуги",
 "sc4": "Митническо представителство или подаване на заявления за лицензи", "sc5": "Финансови или инвестиционни съвети", "sc6": "Услуги по учредяване на дружества",
 "sc_p2": "Когато е необходим официален съвет, препоръчваме независим юрист.",

 "cl_eyebrow": "Клиенти", "cl_h1": "И двете страни на една сделка. Никога едновременно.",
 "cl_lead": "Работим със страните, които носят риска, и с компаниите, които трябва да докажат, че заслужават доверие.",
 "cl1_h": "Западни купувачи", "cl1_p": "Екипи по доставки, качество на доставчиците и съответствие, които въвеждат доставчици в България и на Балканите, както и банките, застрахователите и агентите по снабдяване зад тях.",
 "cl1_w": "Обикновено: Проверка на доставчик, Наблюдение.",
 "cl2_h": "Отбранителни програми", "cl2_p": "Главни изпълнители, интегратори и техните български и балкански доставчици по програми, финансирани от ЕС и НАТО, които се нуждаят от издържани доказателства за собственост и произход.",
 "cl2_w": "Обикновено: Доказателства за отбранителни вериги на доставки.",
 "cl3_h": "Български и балкански износители", "cl3_p": "Производители, търговци и спедитори, които продават на изток и юг или доставят на западни клиенти и се нуждаят от контроли и документи, доказващи, че са сигурен контрагент.",
 "cl3_w": "Обикновено: Готовност за санкционно съответствие, Наблюдение.",
 "cl_note": "Никога не действаме за купувача и доставчика по една и съща сделка. Всеки ангажимент се вписва в дневник.",
 "pr_eyebrow": "Принципи", "pr_h2": "Независими. Не се купуваме.",
 "pr_lead": "Докладите ни струват нещо, защото никой не може да купи различен отговор. Не сме посредник за достъп и не продаваме запознанства, влияние или ускоряване на процедури.",
 "t_h1": "Посредници за достъп", "t_h2": "{B}",
 "t_r1": "Продават", "t_a1": "Достъп и резултати", "t_b1": "Увереност и готовност",
 "t_r2": "Основен актив", "t_a2": "Контакти", "t_b2": "Метод, доказателства, независимост",
 "t_r3": "Плаща", "t_a3": "Който иска резултата", "t_b3": "Страната, която носи риска",
 "t_r4": "Възнаграждение", "t_a4": "Често зависи от успеха", "t_b4": "Фиксирано. Никога условно.",
 "p1": "<b>Само фиксирани такси.</b> Без възнаграждение при успех, без условни плащания и без плащания към или чрез длъжностни лица.",
 "p2": "<b>Без заобикаляне.</b> Не помагаме на никого да избегне експортен контрол, санкции или проверки за крайна употреба и се отказваме от клиенти, които го поискат.",
 "p3": "<b>Само законни източници.</b> Отворени източници, регистри и документи, предоставени от клиента. Без скрито събиране на информация.",
 "p4": "<b>Градирани доказателства.</b> Всяка констатация е маркирана като потвърдена, вероятна или възможна, а фактите са отделени от изводите.",
 "p5": "<b>Управление на конфликти.</b> Само една страна по сделка. Карантинен период и писмено разкриване преди каквато и да е по-късна заинтересованост в сектор, по който сме консултирали.",

 "ab_eyebrow": "За нас", "ab_h1": "Търговски пункт с правила.",
 "ab_lead": "{B} съществува, защото положението на България на югоизточния ръб на ЕС има стойност само ако търгуващите през него си вярват.",
 "an_h": "Името",
 "an_p1": "Пистирос е търговски пункт (емпорион) в долината на Марица, край днешния Ветрен в Южна България, действал от V век пр. Хр. Търговци от гръцките градове Тасос, Маронея и Аполония търгуват там с траките под закрилата на одриските царе.",
 "an_p2": "През 1990 г. археолозите откриват там каменен надпис с царска клетва към тези търговци: дълговете към тях няма да бъдат опрощавани, земята им няма да им бъде отнемана, а споровете им ще се решават от техни сънародници. Това е ранно свидетелство от българските земи за владетел, който гарантира правилата на търговията. Двадесет и четири века по-късно идеята е същата и тя е нашата работа: един кръстопът струва толкова, колкото доверието и правилата, които може да предложи.",
 "ap_h": "Проблемът, който решаваме",
 "ap_p1": "След присъединяването към еврозоната и Шенген България е естествен вход между ЕС и Турция, Кавказ, Централна Азия и Персийския залив. Но западен купувач, който въвежда доставчик тук, все още трудно разбира кой наистина го притежава, къде отиват стоките му и дали сертификатите му са истински. Способните местни компании имат обратния проблем: те са надеждни, но не могат да го покажат във вида, който очаква западният екип по съответствие.",
 "ap_p2": "Обичайните варианти не пасват. Големите фирми са ценово ориентирани към големи поръчки. Местните „решавачи“ продават достъп, а това е точно онова, което внимателният купувач не иска. Ние запълваме празнината: независима работа, основана на доказателства, срещу фиксирана такса, за страната, която носи риска.",
 "pr_h": "Основател",
 "bio_name": "Стефан Бончев", "bio_role": "Основател, {B}",
 "bio_p1": "Стефан има над осем години опит в институционални финанси, счетоводство и операции в Лондон — в Jefferies, PVH, Ripple и BenevolentAI, както и в инвестиционни операции за частни семейни офиси и във финанси в развиващи се пазари. Има магистърска степен (MA) по финанси и испански и работи на английски, български и испански.",
 "bio_p2": "Този опит е работата на фирмата. Кой какво притежава, дали числата и контролите издържат и как реално се движат парите са въпросите, които западният купувач и неговата банка задават на доставчик от границата на ЕС. Стефан цялата си кариера отговаря на тях от страната на операциите, където документите трябва да са точни.",

 "cl_pr_link": "Прочетете принципите ни →",
 "ins_eyebrow": "Анализи", "ins_h1": "Бележки за региона.",
 "ins_lead": "Пазарни доклади и регионални обзори за България, Балканите и маршрутите към Турция, Кавказ и Централна Азия, които помагат на купувачите и компаниите да разберат средата, в която търгуват.",
 "ins_empty_h": "Първите материали са в подготовка.",
 "ins_empty_p": "Пишете ни, ако искате да ви уведомим, когато излезе първият доклад.",
 "art_note": "Статията е на английски.", "art_back": "← Всички анализи", "art_src": "Източници", "ins_list_h": "Примерни материали",
 "cat_outlook": "Перспектива", "cat_guides": "Ръководства", "cat_risk": "Рискови обзори", "cat_regulatory": "Регулации",
 "cat_sectors": "Секторни анализи", "cat_regional": "Регионални обзори",
 "catd_outlook": "Годишният ни поглед към България като база за доставчици: държавен и контрагентски риск, секторна оценка, коридори, ключови дати и сценарии.",
 "catd_guides": "Практически насоки как да проверите контрагент, да прочетете обществена поръчка и да защитите договор.",
 "catd_risk": "Къде се крият рисковете от санкции, собственост, управление и незаконна търговия и как достигат до веригата на доставки на купувача.",
 "catd_regulatory": "Правила на ЕС и България, които променят задълженията на купувачи и износители: експортен контрол, въглерод, обезлесяване, скрининг на инвестиции, прилагане на санкции.",
 "catd_sectors": "Българските отрасли един по един: какво се произвежда, кой го произвежда и какво да проверите, преди да купите.",
 "catd_regional": "Съседите и коридорите на България, от Румъния и Гърция до Турция, Кавказ, Централна Азия и Украйна.",
 "art_corr": "Всеки факт в тази бележка идва от датиран публичен източник, посочен по-горе. Ако смятате, че нещо е грешно или остаряло, пишете ни и ще го проверим и коригираме своевременно.",
 "art_more": "Още от тази категория", "art_outlook": "Прочетете перспективата за българските доставчици 2026 →",
 "ct_btn": "Пишете ни",
 "pv_sum": "Поверителност",
 "pv_p": "Този сайт няма формуляри, не поставя бисквитки и не използва аналитични инструменти. Ако ни пишете по имейл, използваме адреса и съобщението ви само за да отговорим и да изпълним поискана от вас работа, и не ги споделяме. Сайтът се хоства в GitHub Pages, който може да води обичайни сървърни логове извън нашия контрол.",
 "f1_h": "Отказ от отговорност", "f1_p": "Съдържанието на този сайт е обща информация и не представлява правен, данъчен, финансов, инвестиционен или друг професионален съвет. Четенето му не създава отношения клиент–консултант.",
 "f2_h": "Регулаторен статус", "f2_p": "{B} е консултантска фирма по управление. Не е адвокатска кантора, одиторска фирма или данъчен консултант и не е лицензирана или регулирана от Financial Conduct Authority или друг финансов регулатор.",
 "f3_h": "Независимост", "f3_p": "Приемаме само фиксирани такси, не посредничим за достъп и не действаме за двете страни по една сделка.",
 "f_fine": "Всички права запазени.",
 "s4_h": "Наблюдение",
 "s4_for": "За настоящи клиенти",
 "s4_p": "Доставчиците сменят собственици, клиенти и финансово състояние. Всяко тримесечие проверяваме отново вашите доставчици или клиенти и ви уведомяваме за промени в собствеността, съдебните регистри, санкционния статус и медийните публикации, с опция за годишно посещение на място.",
 "s4_s": "Годишна фиксирана такса за всяка наблюдавана компания.",
}

# --------------------------------------------------------------------------- shared chrome
NAV = [("services.html", "nav_services"), ("clients.html", "nav_clients"), ("principles.html", "nav_principles"),
       ("insights.html", "nav_insights"), ("about.html", "nav_about")]

MARK = ('<svg viewBox="0 0 32 32" aria-hidden="true"><g fill="none" stroke="currentColor" stroke-width="2" '
        'stroke-linecap="round" stroke-linejoin="round"><path d="M5 28h22M8 28V13M24 28V13M16 28v-9"/>'
        '<path d="M8 13Q16 1 24 13"/></g></svg>')
FAVICON = ("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'%3E%3Cg fill='none' "
           "stroke='%231d4e6b' stroke-width='2.4' stroke-linecap='round' stroke-linejoin='round'%3E"
           "%3Cpath d='M5 28h22M8 28V13M24 28V13M16 28v-9'/%3E%3Cpath d='M8 13Q16 1 24 13'/%3E%3C/g%3E%3C/svg%3E")


def head(page):  # `page` = filename whose nav link is highlighted
    cur = ' aria-current="page"'
    links = "".join(
        f'<a href="{h}" data-int data-i18n="{k}"{cur if h == page else ""}>{EN[k]}</a>'
        for h, k in NAV)
    return f'''<header>
  <div class="wrap bar">
    <a class="brand" href="index.html" data-int aria-label="{{B}}">{MARK}<span>{{B}}</span></a>
    <nav aria-label="Main">{links}<a class="nav-cta" href="mailto:{EMAIL}" data-i18n="nav_contact">{EN["nav_contact"]}</a></nav>
    <div class="lang" role="group" aria-label="Language">
      <button type="button" data-lang="en" aria-pressed="true">EN</button>
      <button type="button" data-lang="bg" aria-pressed="false">БГ</button>
    </div>
  </div>
</header>'''


FOOT = f'''<footer>
  <div class="wrap">
    <div class="cols">
      <div><h4 data-i18n="f1_h">{EN["f1_h"]}</h4><p data-i18n="f1_p">{EN["f1_p"]}</p></div>
      <div><h4 data-i18n="f2_h">{EN["f2_h"]}</h4><p data-i18n="f2_p">{EN["f2_p"]}</p></div>
      <div><h4 data-i18n="f3_h">{EN["f3_h"]}</h4><p data-i18n="f3_p">{EN["f3_p"]}</p></div>
    </div>
    <details><summary data-i18n="pv_sum">{EN["pv_sum"]}</summary><p data-i18n="pv_p">{EN["pv_p"]}</p></details>
    <p class="fine">© <span id="yr">2026</span> {{B}}. <span data-i18n="f_fine">{EN["f_fine"]}</span> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>
  </div>
</footer>'''


def t(k):
    return f'data-i18n="{k}">{EN[k]}'


def th(k):
    return f'data-i18n-html="{k}">{EN[k]}'


CTA = f'''<section class="cta-band">
  <div class="wrap">
    <h2 {t("cta_h2")}</h2>
    <p class="lead" {t("cta_lead")}</p>
    <a class="btn primary" href="mailto:{EMAIL}"><span {t("ct_btn")}</span> — {EMAIL}</a>
  </div>
</section>'''


INS_DESC = ("Guides, risk briefs, regulatory notes, sector deep dives and regional briefs on Bulgaria, "
            "the Balkans, Turkey, the Caucasus and Central Asia, written for buyers and compliance teams.")
SITE_DESC = ("Independent supplier verification and market-entry readiness for companies trading across "
             "the EU's south-eastern frontier. Management consulting. Fixed fees only.")


def seo_head(name, title, desc, og_type="website", ld=None):
    url = SITE_URL + ("" if name == "index.html" else name)
    e = lambda s: _html.escape(s, quote=True)
    tags = [f'<meta name="description" content="{e(desc)}">',
            f'<link rel="canonical" href="{url}">',
            f'<meta property="og:title" content="{e(title)}">',
            f'<meta property="og:description" content="{e(desc)}">',
            f'<meta property="og:type" content="{og_type}">',
            f'<meta property="og:url" content="{url}">',
            '<meta property="og:site_name" content="{B}">',
            '<meta property="og:locale" content="en_GB">']
    if name == "index.html":
        tags += [f'<meta name="google-site-verification" content="{GOOGLE_VERIFY}">'] if GOOGLE_VERIFY else []
        tags += [f'<meta name="msvalidate.01" content="{BING_VERIFY}">'] if BING_VERIFY else []
    if ld:
        tags.append('<script type="application/ld+json">' + json.dumps(ld, ensure_ascii=False).replace("</", "<\\/") + "</script>")
    return "\n".join(tags)


def page(name, title_key, body, title_text=None, nav=None, seo=None):
    title = title_text or EN[title_key]
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
{seo or seo_head(name, _html.unescape(title), SITE_DESC)}
<meta name="color-scheme" content="light">
{NOINDEX}
<link rel="icon" href="{FAVICON}">
<link rel="stylesheet" href="site.css">
</head>
<body{f' data-title="{title_key}"' if title_key else ""}>
{head(nav or name)}
<main>
{body}
</main>
{FOOT}
<script src="site.js"></script>
</body>
</html>
'''


# --------------------------------------------------------------------------- pages
PRINCIPLES_BODY = f'''<section class="flush">
  <div class="wrap">
    <table class="tbl">
      <thead><tr><th></th><th {t("t_h1")}</th><th {t("t_h2")}</th></tr></thead>
      <tbody>
        <tr><td {t("t_r1")}</td><td {t("t_a1")}</td><td {t("t_b1")}</td></tr>
        <tr><td {t("t_r2")}</td><td {t("t_a2")}</td><td {t("t_b2")}</td></tr>
        <tr><td {t("t_r3")}</td><td {t("t_a3")}</td><td {t("t_b3")}</td></tr>
        <tr><td {t("t_r4")}</td><td {t("t_a4")}</td><td {t("t_b4")}</td></tr>
      </tbody>
    </table>
    <ul class="pledges">
      {"".join(f'<li {th(f"p{i}")}</li>' for i in range(1, 6))}
    </ul>
  </div>
</section>'''


def service_rows(detailed):
    rows = []
    for i in (1, 2, 3, 4):
        extra = f'<p class="meta" {t(f"s{i}_s")}</p>' if detailed else ""
        rows.append(f'''<article class="svc">
      <span class="num">0{i}</span>
      <div><h3 {t(f"s{i}_h")}</h3><span class="for" {t(f"s{i}_for")}</span></div>
      <div><p {t(f"s{i}_p")}</p>{extra}</div>
    </article>''')
    return "\n    ".join(rows)


HOME = f'''<section class="hero">
  <div class="wrap">
    <span class="eyebrow" {t("h_eyebrow")}</span>
    <h1 {t("h_h1")}</h1>
    <p class="lead" {t("h_lead")}</p>
    <div class="actions">
      <a class="btn primary" href="services.html" data-int {t("h_cta1")}</a>
      <a class="btn" href="mailto:{EMAIL}" {t("h_cta2")}</a>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <span class="eyebrow" {t("why_eyebrow")}</span>
    <h2 {t("why_h2")}</h2>
    <div class="cols2"><p {t("why_p1")}</p><p {t("why_p2")}</p></div>
  </div>
</section>

<section class="tint">
  <div class="wrap">
    <span class="eyebrow" {t("hs_eyebrow")}</span>
    <h2 {t("hs_h2")}</h2>
    <div class="svcs">
    {service_rows(False)}
    </div>
    <p class="more"><a href="services.html" data-int {t("hs_more")}</a></p>
  </div>
</section>

<section>
  <div class="wrap">
    <span class="eyebrow" {t("pl_eyebrow")}</span>
    <h2 {t("pl_h2")}</h2>
    <div class="trio">
      <div><h3 {t("pl1_h")}</h3><p {t("pl1_p")}</p></div>
      <div><h3 {t("pl2_h")}</h3><p {t("pl2_p")}</p></div>
      <div><h3 {t("pl3_h")}</h3><p {t("pl3_p")}</p></div>
    </div>
    <p class="more"><a href="principles.html" data-int {t("pl_more")}</a></p>
  </div>
</section>

{CTA}'''

SAMPLES = f'''<section id="samples">
  <div class="wrap">
    <span class="eyebrow" {t("in_eyebrow")}</span>
    <h2 {t("in_h2")}</h2>
    <p class="lead" {t("in_lead")}</p>
    <div class="trio cards">
      <a class="card" href="downloads/sample-supplier-integrity-assessment.pdf" target="_blank" rel="noopener"><span class="tag" {t("d1_t")}</span><h3 {t("d1_h")}</h3><p {t("d1_p")}</p><span class="go">PDF →</span></a>
      <a class="card" href="downloads/buyer-checklist.pdf" target="_blank" rel="noopener"><span class="tag" {t("d2_t")}</span><h3 {t("d2_h")}</h3><p {t("d2_p")}</p><span class="go">PDF →</span></a>
      <a class="card" href="downloads/corridor-briefing-excerpt.pdf" target="_blank" rel="noopener"><span class="tag" {t("d3_t")}</span><h3 {t("d3_h")}</h3><p {t("d3_p")}</p><span class="go">PDF →</span></a>
    </div>
    <p class="fine-note" {t("in_note")}</p>
  </div>
</section>''' if SHOW_DOWNLOADS else ""

SERVICES = f'''<section class="pagehead">
  <div class="wrap">
    <span class="eyebrow" {t("sv_eyebrow")}</span>
    <h1 {t("sv_h1")}</h1>
    <p class="lead" {t("sv_lead")}</p>
  </div>
</section>

<section class="flush">
  <div class="wrap">
    <div class="steps">
      <div><b {t("m1")}</b><span {t("m1d")}</span></div>
      <div><b {t("m2")}</b><span {t("m2d")}</span></div>
      <div><b {t("m3")}</b><span {t("m3d")}</span></div>
    </div>
    <div class="svcs">
    {service_rows(True)}
    </div>
  </div>
</section>

<section class="tint">
  <div class="wrap">
    <h3 {t("sec_h")}</h3>
    <ul class="chips">
      {"".join(f'<li {t(f"sec{i}")}</li>' for i in range(1, 9))}
    </ul>
  </div>
</section>

{SAMPLES}

<section class="tint scope">
  <div class="wrap">
    <span class="eyebrow" {t("sc_eyebrow")}</span>
    <h2 {t("sc_h2")}</h2>
    <p {t("sc_p")}</p>
    <ul>
      {"".join(f'<li {t(f"sc{i}")}</li>' for i in range(1, 7))}
    </ul>
    <p {t("sc_p2")}</p>
  </div>
</section>

{CTA}'''

CLIENTS = f'''<section class="pagehead">
  <div class="wrap">
    <span class="eyebrow" {t("cl_eyebrow")}</span>
    <h1 {t("cl_h1")}</h1>
    <p class="lead" {t("cl_lead")}</p>
  </div>
</section>

<section class="flush">
  <div class="wrap">
    <div class="trio">
      {"".join(f'<div><h3 {t(f"cl{i}_h")}</h3><p {t(f"cl{i}_p")}</p><p class="meta" {t(f"cl{i}_w")}</p></div>' for i in (1, 2, 3))}
    </div>
    <p class="note" {t("cl_note")}</p>
    <p class="more"><a href="principles.html" data-int {t("cl_pr_link")}</a></p>
  </div>
</section>

{CTA}'''

PRINCIPLES = f'''<section class="pagehead">
  <div class="wrap">
    <span class="eyebrow" {t("pr_eyebrow")}</span>
    <h1 {t("pr_h2")}</h1>
    <p class="lead" {t("pr_lead")}</p>
  </div>
</section>

{PRINCIPLES_BODY}

{CTA}'''

INSIGHTS = f'''<section class="pagehead">
  <div class="wrap">
    <span class="eyebrow" {t("ins_eyebrow")}</span>
    <h1 {t("ins_h1")}</h1>
    <p class="lead" {t("ins_lead")}</p>
  </div>
</section>

<section class="flush">
  <div class="wrap">
__CARDS__
    <p class="fine-note" {t("art_note")}</p>
  </div>
</section>'''

PERSON = f'''<section class="tint">
  <div class="wrap">
    <span class="eyebrow" {t("pr_h")}</span>
    <div class="person">
      <img class="photo" src="stefan.jpg" width="300" height="400" alt="Stefan Bonchev">
      <div>
        <h2 {t("bio_name")}</h2>
        <p class="role" {t("bio_role")}</p>
        <p {t("bio_p1")}</p>
        <p {t("bio_p2")}</p>
      </div>
    </div>
  </div>
</section>''' if SHOW_BIO else ""

ABOUT = f'''<section class="pagehead">
  <div class="wrap">
    <span class="eyebrow" {t("ab_eyebrow")}</span>
    <h1 {t("ab_h1")}</h1>
    <p class="lead" {t("ab_lead")}</p>
  </div>
</section>

<section class="flush">
  <div class="wrap cols2 story">
    <div><h3 {t("an_h")}</h3><p {th("an_p1")}</p><p {th("an_p2")}</p></div>
    <div><h3 {t("ap_h")}</h3><p {t("ap_p1")}</p><p {t("ap_p2")}</p></div>
  </div>
</section>

{PERSON}

{CTA}'''

# --------------------------------------------------------------------------- css / js
CSS = r'''
:root{
  --bg:#fff; --ink:#15202b; --muted:#5b6673; --line:#e4e7eb; --tint:#f6f8fa;
  --accent:#1d4e6b; --accent-ink:#fff;
  --serif:Georgia,"Iowan Old Style","Palatino Linotype",serif;
  --sans:system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
  --max:1040px;
}
*{box-sizing:border-box}
html{scroll-padding-top:80px}
body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.65 var(--sans);-webkit-font-smoothing:antialiased}
a{color:var(--accent)}
.wrap{max-width:var(--max);margin:0 auto;padding:0 24px}
h1,h2,h3{font-family:var(--serif);font-weight:400;line-height:1.18;letter-spacing:-.015em;margin:0 0 .5em}
h1{font-size:clamp(2.3rem,5.4vw,3.8rem)}
h2{font-size:clamp(1.65rem,3.2vw,2.2rem)}
h3{font-size:1.3rem}
p{margin:0 0 1em}
.eyebrow{display:block;font:600 .74rem/1 var(--sans);letter-spacing:.18em;text-transform:uppercase;color:var(--accent);margin-bottom:18px}
.lead{font-size:1.2rem;color:var(--muted);max-width:60ch}
section{padding:88px 0}
section.tint{background:var(--tint);border-block:1px solid var(--line)}
section.flush{padding-top:8px}

header{position:sticky;top:0;z-index:20;background:rgba(255,255,255,.94);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.bar{display:flex;align-items:center;gap:28px;height:68px}
.brand{display:flex;align-items:center;gap:10px;text-decoration:none;color:var(--ink);font:400 1.2rem var(--serif);letter-spacing:.01em}
.brand svg{width:26px;height:26px;color:var(--accent)}
nav{display:flex;align-items:center;gap:26px;margin-left:auto;font-size:.93rem}
nav a{text-decoration:none;color:var(--muted);padding:4px 0;border-bottom:1px solid transparent}
nav a:hover,nav a[aria-current]{color:var(--ink);border-bottom-color:var(--accent)}
nav .nav-cta{color:var(--accent);border:1px solid var(--accent);border-radius:6px;padding:6px 14px}
nav .nav-cta:hover{background:var(--accent);color:var(--accent-ink)}
.lang{display:flex;border:1px solid var(--line);border-radius:6px;overflow:hidden}
.lang button{border:0;background:transparent;color:var(--muted);font:600 .78rem var(--sans);padding:6px 10px;cursor:pointer}
.lang button[aria-pressed="true"]{background:var(--ink);color:#fff}
@media (max-width:760px){.bar{gap:12px}nav{gap:14px;font-size:.84rem}nav .nav-cta{display:none}.brand span{display:none}}

.hero{padding:120px 0 104px}
.hero h1{max-width:17ch;font-size:clamp(2.6rem,6.4vw,4.6rem)}
.hero .lead{margin-top:26px}
.actions{display:flex;flex-wrap:wrap;gap:12px;margin-top:36px}
.btn{display:inline-block;padding:13px 24px;border-radius:6px;text-decoration:none;font-weight:600;font-size:.95rem;border:1px solid var(--ink);color:var(--ink)}
.btn:hover{background:var(--tint)}
.btn.primary{background:var(--accent);border-color:var(--accent);color:var(--accent-ink)}
.btn.primary:hover{filter:brightness(1.12)}
.pagehead{padding:96px 0 56px}
.pagehead h1{max-width:20ch}
.pagehead .lead{margin-top:20px}

.cols2{display:grid;grid-template-columns:1fr 1fr;gap:12px 56px}
@media (max-width:760px){.cols2{grid-template-columns:1fr}}
.story h3{margin-bottom:.7em}
.trio{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:36px;margin-top:30px}
.trio h3{padding-top:16px;border-top:2px solid var(--accent)}
.trio p{color:var(--muted)}
.meta{font-size:.88rem;color:var(--muted)}
.empty{border:1px dashed var(--line);border-radius:8px;padding:44px 32px;text-align:center;background:var(--tint)}
.empty p{color:var(--muted);max-width:52ch;margin:0 auto 22px}
.prose>*{max-width:700px}
.prose h2{font-size:1.45rem;margin:2em 0 .5em}
.prose p,.prose li{color:#2a3744}
.prose ul{padding-left:1.2em;margin:0 0 1.2em}
.prose li{margin-bottom:.45em}
.prose h3{font-size:1.15rem;margin:1.6em 0 .4em}
.prose ol{padding-left:1.4em;margin:0 0 1.2em}
.prose .tblwrap{max-width:100%;overflow-x:auto;margin:24px 0}
.prose .tbl.art{margin:0;font-size:.9rem}
.prose .tbl.art td:first-child{width:auto;color:var(--ink);font-weight:600}
.prose .tbl.art td:nth-child(3){font-weight:400;color:inherit}
.srcs{margin-top:3em;padding-top:1em;border-top:1px solid var(--line);font-size:.82rem;color:var(--muted)}
.srcs h2{font-size:1.1rem}
.srcs ul{padding-left:1.1em}
.srcs li{color:var(--muted);word-break:break-all}
.more{margin-top:30px;font-weight:600}
.more a{text-decoration:none}
.note{margin-top:44px;color:var(--muted);max-width:62ch}

.svcs{border-top:1px solid var(--line);margin-top:30px}
.svc{display:grid;grid-template-columns:56px 1fr 1.5fr;gap:12px 32px;padding:34px 0;border-bottom:1px solid var(--line)}
.svc .num{font:400 1.1rem var(--serif);color:var(--accent);padding-top:4px}
.svc h3{margin-bottom:.25em}
.svc .for{font-size:.9rem;color:var(--muted)}
.svc p{color:var(--muted)}
@media (max-width:760px){.svc{grid-template-columns:1fr;gap:6px}}

.steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:0;border:1px solid var(--line);border-radius:8px;overflow:hidden}
.steps div{padding:22px 26px;border-right:1px solid var(--line)}
.steps div:last-child{border-right:0}
.steps b{display:block;font:400 1.3rem var(--serif);margin-bottom:6px;color:var(--accent)}
.steps span{color:var(--muted);font-size:.95rem;display:block}
@media (max-width:700px){.steps div{border-right:0;border-bottom:1px solid var(--line)}.steps div:last-child{border-bottom:0}}

.chips{display:flex;flex-wrap:wrap;gap:10px;padding:0;margin:22px 0 0;list-style:none}
.chips li{border:1px solid var(--line);background:#fff;padding:8px 16px;border-radius:999px;font-size:.93rem}

.cards .card{display:flex;flex-direction:column;gap:4px;text-decoration:none;color:var(--ink);border:1px solid var(--line);border-radius:8px;padding:24px;background:#fff}
.cards .card:hover{border-color:var(--accent)}
.cards .card h3{border:0;padding:0;font-size:1.15rem}
.cards .card p{color:var(--muted);font-size:.95rem}
.tag{font:600 .72rem var(--sans);letter-spacing:.14em;text-transform:uppercase;color:var(--accent)}
.go{margin-top:auto;padding-top:10px;font-weight:600;font-size:.9rem;color:var(--accent)}
.fine-note{margin-top:18px;font-size:.88rem;color:var(--muted)}
.catnav{margin:0 0 8px}
.catnav a{text-decoration:none;color:var(--ink)}
.catnav li:hover{border-color:var(--accent)}
.catsec{padding-top:56px;scroll-margin-top:80px}
.catsec h2{margin-bottom:.2em}
.catsec .lead{font-size:1.02rem}
.cards.feature{grid-template-columns:1fr}
.cards.feature .card{background:var(--tint);border-color:var(--accent)}
.cards.feature .card h3{font-size:1.5rem}
a.eyebrow{text-decoration:none}
.morecat{margin-top:3em;padding-top:1em;border-top:1px solid var(--line)}
.morecat h2{font-size:1.1rem}
.morecat ul{padding-left:1.1em}
.prose li.check{list-style:none;position:relative}
.prose li.check::before{content:"";position:absolute;left:-1.35em;top:.3em;width:.8em;height:.8em;border:1.5px solid var(--accent);border-radius:2px}

.tbl{width:100%;border-collapse:collapse;background:#fff;border:1px solid var(--line);font-size:.96rem;margin:30px 0}
.tbl th,.tbl td{padding:14px 18px;text-align:left;border-bottom:1px solid var(--line);vertical-align:top}
.tbl tr:last-child td{border-bottom:0}
.tbl th{font:600 .78rem var(--sans);letter-spacing:.1em;text-transform:uppercase;color:var(--muted);background:var(--tint)}
.tbl td:first-child{color:var(--muted);width:20%}
.tbl td:nth-child(3){font-weight:600;color:var(--accent)}
@media (max-width:640px){.tbl th,.tbl td{padding:10px;font-size:.86rem}}
.pledges{list-style:none;padding:0;margin:0;display:grid;gap:14px}
.pledges li{padding-left:30px;position:relative}
.pledges li::before{content:"";position:absolute;left:0;top:.8em;width:16px;height:2px;background:var(--accent)}

.scope ul{columns:2;column-gap:40px;padding-left:1.1em;margin:14px 0 18px}
@media (max-width:640px){.scope ul{columns:1}}
.scope li{margin-bottom:6px;break-inside:avoid}

.person{display:grid;grid-template-columns:300px 1fr;gap:48px;align-items:start;margin-top:6px}
@media (max-width:760px){.person{grid-template-columns:1fr;gap:24px}.photo{max-width:260px}}
.photo{width:100%;height:auto;border-radius:6px;border:1px solid var(--line);display:block}
.role{color:var(--muted);margin-bottom:1.2em}

.cta-band{text-align:center;border-top:1px solid var(--line)}
.cta-band .lead{margin:0 auto 28px}

footer{background:var(--tint);border-top:1px solid var(--line);padding:48px 0 36px;font-size:.84rem;line-height:1.6;color:var(--muted)}
footer h4{margin:0 0 8px;font:600 .72rem var(--sans);letter-spacing:.14em;text-transform:uppercase;color:var(--ink)}
footer .cols{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:28px;margin-bottom:26px}
footer p{margin:0}
footer details{margin-bottom:22px}
footer summary{cursor:pointer;color:var(--ink);font-weight:600}
footer details p{margin-top:8px;max-width:70ch}
footer .fine{border-top:1px solid var(--line);padding-top:18px}
footer a{color:var(--muted)}
:focus-visible{outline:2px solid var(--accent);outline-offset:3px}
'''

JS = r'''(function(){
var T = __DICT__;
var KEY="pistiros_lang";
function setLang(l){
  if(!T[l]) l="en";
  document.documentElement.lang=l;
  document.querySelectorAll("[data-i18n]").forEach(function(el){var v=T[l][el.dataset.i18n]; if(v!==undefined) el.textContent=v;});
  document.querySelectorAll("[data-i18n-html]").forEach(function(el){var v=T[l][el.dataset.i18nHtml]; if(v!==undefined) el.innerHTML=v;});
  document.querySelectorAll(".lang button").forEach(function(b){b.setAttribute("aria-pressed", b.dataset.lang===l?"true":"false");});
  document.querySelectorAll("a[data-int]").forEach(function(a){
    var h=a.getAttribute("href").split("#")[0]; var hash=a.getAttribute("href").split("#")[1];
    a.setAttribute("href", h + (l==="bg" ? "#bg" : (hash?"#"+hash:"")));
  });
  var tk=document.body.dataset.title; if(tk&&T[l][tk]) document.title=T[l][tk];
  try{localStorage.setItem(KEY,l);}catch(e){}
  try{history.replaceState(null,"",location.pathname+location.search+(l==="bg"?"#bg":""));}catch(e){}
}
function initial(){
  var q=(location.search.match(/[?&]lang=(\w\w)/)||[])[1];
  if(q && T[q]) return q;
  if(location.hash==="#bg") return "bg";
  try{var s=localStorage.getItem(KEY); if(s&&T[s]) return s;}catch(e){}
  return (navigator.language||"").toLowerCase().indexOf("bg")===0 ? "bg":"en";
}
document.querySelectorAll(".lang button").forEach(function(b){b.addEventListener("click",function(){setLang(b.dataset.lang);});});
document.getElementById("yr").textContent=new Date().getFullYear();
setLang(initial());
})();
'''


def sub(s):
    return s.replace("{B}", BRAND)


def _inline(x):
    x = _html.escape(x, quote=False)
    x = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', x)
    x = re.sub(r"\[([^\]]+)\]\((insight-[\w-]+\.html)\)", r'<a href="\2" data-int>\1</a>', x)
    x = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", x)
    x = re.sub(r'(?<!["\'>=])(https?://[^\s<)]+)', r'<a href="\1" target="_blank" rel="noopener">\1</a>', x)
    return x


def parse_article(path):
    lines = path.read_text(encoding="utf-8").splitlines()
    title = lines[0].lstrip("# ").strip()
    summary = published = date = cat = ""
    body, srcs, cur, para, in_src = [], [], None, [], False
    out = []

    def flush():
        nonlocal para
        if para:
            out.append("<p>" + _inline(" ".join(para)) + "</p>")
            para = []

    def close_ul():
        nonlocal cur
        if cur:
            out.append(f"</{cur}>")
            cur = None

    def close_tbl():  # markdown pipe table -> scrollable table
        nonlocal tbl
        if tbl:
            rows = [[c.strip() for c in r.strip().strip("|").split("|")] for r in tbl
                    if not re.fullmatch(r"[\s:|-]+", r)]
            h = "".join(f"<th>{_inline(c)}</th>" for c in rows[0])
            b = "".join("<tr>" + "".join(f"<td>{_inline(c)}</td>" for c in r) + "</tr>" for r in rows[1:])
            out.append(f'<div class="tblwrap"><table class="tbl art"><thead><tr>{h}</tr></thead><tbody>{b}</tbody></table></div>')
            tbl = []

    tbl = []
    for ln in lines[1:]:
        if ln.startswith("|") and not in_src:
            flush(); close_ul(); tbl.append(ln); continue
        close_tbl()
        if ln.startswith("Summary:"):
            summary = ln[8:].strip(); continue
        if ln.startswith("Published:"):
            published = ln[10:].strip(); continue
        if ln.startswith("Date:"):
            date = ln[5:].strip(); continue
        if ln.startswith("Category:"):
            cat = ln[9:].strip(); continue
        if ln.startswith("### "):
            flush(); close_ul()
            out.append(f"<h3>{_inline(ln[4:].strip())}</h3>"); continue
        if ln.startswith("## "):
            flush(); close_ul()
            in_src = ln[3:].strip().lower() == "sources"
            if not in_src:
                out.append(f"<h2>{_inline(ln[3:].strip())}</h2>")
            else:
                out.append("__SOURCES__")
            continue
        if ln.startswith("- "):
            flush()
            if in_src:
                srcs.append(ln[2:].strip()); continue
            if cur != "ul":
                close_ul(); out.append("<ul>"); cur = "ul"
            item = ln[2:].strip()
            if item.startswith("[ ] "):  # checklist item
                out.append('<li class="check">' + _inline(item[4:]) + "</li>"); continue
            out.append("<li>" + _inline(item) + "</li>"); continue
        m = re.match(r"\d+\. (.*)", ln)
        if m and not in_src:
            flush()
            if cur != "ol":
                close_ul(); out.append("<ol>"); cur = "ol"
            out.append("<li>" + _inline(m.group(1).strip()) + "</li>"); continue
        if not ln.strip():
            flush(); close_ul(); continue
        if in_src:
            srcs.append(ln.strip()); continue
        para.append(ln.strip())
    flush(); close_ul(); close_tbl()
    html_body = "\n".join(out)
    if "__SOURCES__" in html_body:
        src_html = (f'<section class="srcs"><h2 data-i18n="art_src">{EN["art_src"]}</h2><ul>'
                    + "".join(f"<li>{_inline(x)}</li>" for x in srcs) + "</ul></section>") if any("http" in x for x in srcs) else \
                   (f'<section class="srcs"><h2 data-i18n="art_src">{EN["art_src"]}</h2><p>' + _inline(" ".join(srcs)) + "</p></section>")
        html_body = html_body.replace("__SOURCES__", "")
    else:
        src_html = ""
    assert cat in CATEGORIES, f"{path.name}: missing or unknown Category"
    return dict(title=title, summary=summary, published=published, date=date, cat=cat, body=html_body, src=src_html)


def article_page(a, more):
    c = a["cat"]
    more_html = ""
    if more:
        items = "".join(f'<li><a href="insight-{m["slug"]}.html" data-int>{_html.escape(m["title"])}</a></li>' for m in more)
        more_html = f'<section class="morecat"><h2 {t("art_more")}</h2><ul>{items}</ul></section>'
    outlook = "" if c == "outlook" else \
        f'<p class="more"><a href="insight-bulgarian-supplier-outlook-2026.html" data-int {t("art_outlook")}</a></p>'
    return f"""<section class="pagehead">
  <div class="wrap">
    <a class="eyebrow" href="insights.html#{c}" data-i18n="cat_{c}">{EN["cat_" + c]}</a>
    <h1>{_html.escape(a["title"])}</h1>
    <p class="lead">{_html.escape(a["summary"])}</p>
    <p class="meta">{_html.escape(a["published"])} · <span data-i18n="art_note">{EN["art_note"]}</span></p>
  </div>
</section>

<section class="flush">
  <div class="wrap prose">
{a["body"]}
{a["src"]}
    <p class="fine-note" {t("art_corr")}</p>
{more_html}
{outlook}
    <p class="more"><a href="insights.html" data-int {t("art_back")}</a></p>
  </div>
</section>

{CTA}"""


def _desc(text, n=158):  # meta description: summary cut at a word boundary
    return text if len(text) <= n else text[:n].rsplit(" ", 1)[0].rstrip(",;:") + "…"


def _card(a):
    return (f'<a class="card" href="insight-{a["slug"]}.html" data-int>'
            f'<span class="tag" data-i18n="cat_{a["cat"]}">{EN["cat_" + a["cat"]]}</span>'
            f'<h3>{_html.escape(a["title"])}</h3><p>{_html.escape(a["summary"])}</p><span class="go">→</span></a>')


def load_articles():
    arts = []
    for f in INSIGHTS_SRC.glob("*.md"):
        a = parse_article(f)
        m = re.match(r"(\d+)-insight-(.+)", f.stem)
        a["slug"] = m.group(2) if m else f.stem
        a["order"] = (CATEGORIES.index(a["cat"]), 1 if m else 0, int(m.group(1)) if m else 0, f.stem)
        arts.append(a)
    return sorted(arts, key=lambda a: a["order"])


def build_insights():
    arts = load_articles()
    pages = {}
    for i, a in enumerate(arts):
        fname = f"insight-{a['slug']}.html"
        # nearest neighbours in reading order, so every note is linked from others in its category
        same = [b for b in arts if b["cat"] == a["cat"] and b is not a]
        more = sorted(same, key=lambda b: abs(arts.index(b) - i))[:4]
        ld = {"@context": "https://schema.org", "@type": "Article", "headline": a["title"],
              "description": a["summary"], "datePublished": a["date"], "dateModified": a["date"],
              "inLanguage": "en", "articleSection": EN["cat_" + a["cat"]],
              "mainEntityOfPage": SITE_URL + fname,
              "author": {"@type": "Organization", "name": BRAND, "url": SITE_URL},
              "publisher": {"@type": "Organization", "name": BRAND, "url": SITE_URL}}
        seo = seo_head(fname, a["title"], _desc(a["summary"]), "article", ld)
        pages[fname] = sub(page(fname, None, article_page(a, more), nav="insights.html", seo=seo,
                                title_text=f"{_html.escape(a['title'])} | {{B}}"))
    # index page: category jump links, then one section per category
    nav = "".join(f'<li><a href="#{c}" data-i18n="cat_{c}">{EN["cat_" + c]}</a></li>'
                  for c in CATEGORIES if any(a["cat"] == c for a in arts))
    secs = [f'    <ul class="chips catnav">{nav}</ul>']
    for c in CATEGORIES:
        group = [a for a in arts if a["cat"] == c]
        if not group:
            continue
        cls = "trio cards feature" if c == "outlook" else "trio cards"
        secs.append(f'    <div class="catsec" id="{c}">\n'
                    f'      <h2 data-i18n="cat_{c}">{EN["cat_" + c]}</h2>\n'
                    f'      <p class="lead" data-i18n="catd_{c}">{EN["catd_" + c]}</p>\n'
                    f'      <div class="{cls}">{"".join(_card(a) for a in group)}</div>\n'
                    f'    </div>')
    return pages, "\n".join(secs)


def write_sitemap(names):
    rows = "".join(f"<url><loc>{SITE_URL}{'' if n == 'index.html' else n}</loc></url>\n" for n in names)
    (OUT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n'
                                     '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                     + rows + "</urlset>\n", encoding="utf-8")


def main():
    OUT.mkdir(exist_ok=True)
    ipages, cards = build_insights()
    for fn, h in ipages.items():
        (OUT / fn).write_text(h, encoding="utf-8")
    for fname, key, body in [("index.html", "title_home", HOME), ("services.html", "title_services", SERVICES),
                             ("clients.html", "title_clients", CLIENTS), ("principles.html", "title_principles", PRINCIPLES),
                             ("insights.html", "title_insights", INSIGHTS), ("about.html", "title_about", ABOUT)]:
        seo = seo_head(fname, sub(EN[key]), INS_DESC) if fname == "insights.html" else None
        (OUT / fname).write_text(sub(page(fname, key, body, seo=seo)).replace("__CARDS__", cards), encoding="utf-8")
    main_pages = ["index.html", "services.html", "clients.html", "principles.html", "insights.html", "about.html"]
    write_sitemap(main_pages + list(ipages))
    robots = OUT / "robots.txt"  # a GitHub Pages project site cannot serve robots.txt at the domain root anyway
    if PREVIEW:
        robots.write_text("User-agent: *\nDisallow: /\n", encoding="utf-8")
    elif robots.exists():
        robots.unlink()
    (OUT / "site.css").write_text(CSS.strip() + "\n", encoding="utf-8")
    d = {l: {k: sub(v) for k, v in dd.items() if SHOW_BIO or not k.startswith(("bio_", "pr_h"))
             or k in ("pr_h2",)} for l, dd in (("en", EN), ("bg", BG))}
    missing = set(EN) ^ set(BG)
    assert not missing, missing
    (OUT / "site.js").write_text(JS.replace("__DICT__", json.dumps(d, ensure_ascii=False)), encoding="utf-8")
    if SHOW_BIO:
        import shutil
        shutil.copy(ROOT / "assets" / "stefan.jpg", OUT / "stefan.jpg")
    print("built", [p.name for p in OUT.glob("*.html")])


if __name__ == "__main__":
    main()
