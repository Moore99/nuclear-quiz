# Nuclear Quiz — Development Branch (Flutter App)

## Overview

The development branch transforms Nuclear Quiz from a local Flask web app into a cross-platform mobile application for the Google Play Store and Apple App Store. Built with Flutter, it targets nuclear industry professionals, students, and enthusiasts on Android and iOS. The app monetizes via Google AdMob with an optional in-app purchase to remove ads permanently, and uses the same backend infrastructure, authentication patterns, and tooling already proven in the nuclear-motd-mobile project.

---

## Technical Stack

The stack mirrors nuclear-motd-mobile directly to minimize learning overhead and maximize code reuse:

- **Framework**: Flutter (Dart ≥ 3.2.0)
- **State Management**: flutter_riverpod
- **Navigation**: go_router
- **Networking**: Dio with JWT AuthInterceptor (same pattern as nuclear-motd)
- **Local Storage**: flutter_secure_storage (tokens, biometric credential flag), Hive (cached stats/results), shared_preferences (lightweight flags)
- **Auth**: JWT via nuclear-motd server + local_auth for biometric unlock
- **Ads**: google_mobile_ads (banner + native, reuse existing AdMob account ca-app-pub-5119215558360251)
- **IAP**: in_app_purchase (Flutter plugin) for "Remove Ads" one-time purchase
- **Analytics**: firebase_analytics + firebase_crashlytics (same Firebase project as nuclear-motd or a new one)
- **Notifications**: firebase_messaging (optional — quiz reminders)
- **CI/CD**: Codemagic (same workflow as nuclear-motd — push to GitHub, trigger build, auto-distribute to TestFlight/Play Internal)

---

## Backend API (nuclear-motd.com orphaned endpoints)

Add the following routes to the nuclear-motd server. They are "orphaned" — not linked from the main nuclear-motd UI — but publicly accessible for the app and for store-required legal pages.

### Quiz API Endpoints

```
POST   /quiz/auth/register         — Create account (username, email, password)
POST   /quiz/auth/login            — Login, returns JWT
POST   /quiz/auth/forgot-password  — Trigger reset email
POST   /quiz/auth/reset-password   — Submit new password with token

GET    /quiz/categories            — List all categories with question counts
GET    /quiz/questions?category_id=&limit=10  — Fetch randomized question set
POST   /quiz/results               — Submit quiz result (user_id, category_id, score, total, answers[])
GET    /quiz/progress              — Authenticated: per-category stats for current user
GET    /quiz/leaderboard?category_id=  — Top scores (optional, see recommendations)

GET    /quiz/iap/verify            — Verify in-app purchase receipt (Android/iOS), set user ad-free flag
```

### Legal Pages (orphaned, publicly accessible, required by stores)

```
GET    /quiz/privacy-policy        — Returns HTML privacy policy page
GET    /quiz/terms                 — Returns HTML terms & conditions page
```

These two routes serve static or semi-static HTML pages. They satisfy the App Store and Play Store requirement that privacy policy and terms URLs be publicly accessible and not require login. Host them under the nuclear-motd domain so no additional infrastructure is needed.

---

## Features

### Authentication & Biometric Login

Users register and log in with email and password. On successful login, the JWT and encrypted credentials are stored in flutter_secure_storage (same dual-store pattern as nuclear-motd: SecureStorage primary, SharedPreferences backup). On subsequent app launches, the app checks for a stored token and, if biometrics are available and the user has opted in, presents Face ID / fingerprint instead of the full login form. The `local_auth` package handles this — it is already a dependency in nuclear-motd-mobile and proven working.

Biometric opt-in is a toggle in Profile settings. It does not replace the server-side JWT; it only gates the local credential retrieval. If biometric fails three times, the app falls back to the standard login screen.

### Quiz Flow

The home screen shows categories with question counts (same data as the Flask app). Tapping a category starts a quiz session: 10 random questions are fetched from the API, served one at a time, with immediate feedback and explanation after each answer. A summary screen at the end shows score, percentage, and a full review. Results are POSTed to the server so stats persist across devices and logins.

### Stats Persistence

All quiz results are stored server-side under the user's account (POST /quiz/results). The Progress screen retrieves per-category accuracy, total questions answered, streaks, and best scores via GET /quiz/progress. Results are also cached locally in Hive so the Progress screen loads instantly without waiting for the network, then refreshes in the background.

### AdMob Integration

Reuse the existing AdMob account (ca-app-pub-5119215558360251) already set up for nuclear-motd. Create new ad units for Nuclear Quiz in the AdMob console. Ad placement follows the same unobtrusive approach used in nuclear-motd:

- **Banner ad**: shown at the bottom of the home/category screen only — never during a quiz question (it breaks focus and degrades the experience)
- **Native ad**: inserted into the results review list after every 5 questions, using the same ListTileNativeAdFactory already implemented in MainActivity.kt and AppDelegate.swift
- **Interstitial ad**: shown once on the results summary screen, after the score is displayed and the user has had a moment to see their result — not on every quiz, only every 3rd completion to avoid fatigue

No ads appear during active quiz questions. This is both a better user experience and aligns with AdMob policy around not placing ads in ways that cause accidental clicks.

### Remove Ads (In-App Purchase)

A "Remove Ads" option is available in the Profile screen as a one-time purchase (suggested price: $2.99 USD). Use the `in_app_purchase` Flutter plugin. On successful purchase:

1. The receipt is sent to POST /quiz/iap/verify on the server, which validates with Google/Apple and sets an `ads_removed` flag on the user's account.
2. The flag is also stored locally in flutter_secure_storage.
3. All ad widgets check this flag before rendering — if set, they render empty SizedBox widgets.

The server-side flag means the purchase is honoured across reinstalls and device switches as long as the user logs in. A "Restore Purchase" button (required by Apple) triggers the same verification flow using the existing purchase history.

### Analytics

Firebase Analytics tracks:

- `quiz_started` (category_id, category_name)
- `quiz_completed` (category_id, score, total, percentage)
- `question_answered` (category_id, is_correct)
- `ad_removed_purchased`
- `biometric_enabled` / `biometric_disabled`
- Screen views (automatic via FirebaseAnalytics.logScreenView)

Firebase Crashlytics captures crashes and non-fatal errors automatically. Use the same initialization pattern as nuclear-motd (Firebase.initializeApp() in main.dart, do NOT call FirebaseApp.configure() in AppDelegate.swift — this causes a SIGABRT crash on iOS).

---

## Project Structure

Follow the same feature-based structure as nuclear-motd-mobile:

```
lib/
├── core/
│   ├── config/
│   │   └── app_config.dart          # API base URL, ad unit IDs, IAP product IDs
│   ├── network/
│   │   └── dio_client.dart          # Dio + AuthInterceptor (copy from nuclear-motd, change base URL)
│   ├── router/
│   │   └── app_router.dart          # go_router config
│   ├── services/
│   │   ├── biometric_service.dart   # local_auth wrapper
│   │   ├── iap_service.dart         # in_app_purchase wrapper
│   │   └── analytics_service.dart   # Firebase Analytics wrapper
│   ├── cache/
│   │   └── quiz_cache_service.dart  # Hive-backed results/progress cache
│   └── theme/
│       └── app_theme.dart
├── features/
│   ├── auth/                        # login, register, forgot password, biometric prompt
│   ├── home/                        # category list
│   ├── quiz/                        # quiz flow: question screen, submit, results
│   ├── progress/                    # per-category stats, history
│   ├── leaderboard/                 # (optional) top scores
│   ├── profile/                     # settings, remove ads, restore purchase, biometric toggle
│   │   └── screens/
│   │       ├── privacy_policy_screen.dart
│   │       └── terms_screen.dart
│   └── shared/
│       └── widgets/
│           ├── banner_ad_widget.dart
│           ├── native_ad_widget.dart
│           └── offline_banner.dart
└── main.dart
```

---

## App Store Requirements

### Privacy Policy

Host at: `https://nuclear-motd.com/quiz/privacy-policy`

Key disclosures required for both stores:

- **Data collected**: Email address, username, quiz results, device identifiers (for AdMob)
- **Purpose**: Account management, personalized quiz progress, advertising (AdMob), crash reporting (Firebase)
- **Third parties**: Google AdMob (advertising), Google Firebase (analytics, crash reporting, auth)
- **AdMob**: Disclose that the app uses interest-based advertising; include link to Google's privacy policy; disclose that users can opt out via device ad settings
- **Biometrics**: Biometric data is processed locally by the device OS only; the app never transmits biometric data to any server
- **Data retention**: Account data retained until account deletion; anonymized analytics retained per Firebase defaults
- **Children**: App is not directed to children under 13 (COPPA); users must be 13+ to register
- **GDPR / PIPEDA**: Same disclosures as nuclear-motd privacy policy
- **Contact**: Use same privacy@nuclear-motd.com or create quiz@nuclear-motd.com
- **Deletion**: Users can request account deletion from Profile screen or by email

### Terms & Conditions

Host at: `https://nuclear-motd.com/quiz/terms`

Key sections:

- **Acceptance**: By using the app, users agree to these terms
- **Eligibility**: Must be 13+ to use; 18+ or parental consent for IAP
- **Account**: User responsible for credentials; one account per person
- **Quiz content**: Questions are for educational purposes only; not a substitute for professional training, regulatory guidance, or certified qualification programs
- **In-App Purchase**: Remove Ads is a one-time non-refundable purchase (follow Apple/Google refund policy language); no subscription
- **Intellectual Property**: All quiz content, branding, and code are property of Kernkraft Consulting Inc.
- **Disclaimer**: Quiz results do not constitute professional certification; accuracy of content is provided in good faith but not warranted
- **Termination**: Kernkraft reserves the right to suspend accounts for abuse
- **Governing Law**: Ontario, Canada
- **Changes**: Terms may be updated; continued use constitutes acceptance

### App Store Metadata

- **Category**: Education
- **Age Rating**: 4+ (no objectionable content; AdMob requires disclosing ads to Apple)
- **Content Rating (Google)**: Everyone
- **Keywords**: nuclear, reactor, quiz, CANDU, radiation, safety, training, study
- **Short Description (Play)**: Test your nuclear science knowledge — quizzes on CANDU systems, radiation protection, IAEA standards, and more.

---

## Additional Recommendations

**Daily quiz reminder notifications.** Firebase Messaging can send a daily push notification ("Your nuclear knowledge quiz is ready") at a user-chosen time, similar to nuclear-motd's scheduled message feature. This dramatically improves retention metrics and is straightforward given Firebase is already integrated.

**Streak tracking.** Record the user's consecutive days with at least one completed quiz on the server. Display a streak counter on the home screen (like Duolingo). This is a zero-cost engagement mechanic that significantly improves daily active user numbers, which in turn improves AdMob revenue.

**Dark mode.** Trivial to implement in Flutter. Nuclear industry professionals often work in control rooms with controlled lighting; dark mode will be appreciated. Use the same AppTheme pattern from nuclear-motd.

**Offline mode for previously-fetched questions.** Cache the most recently fetched question set in Hive so users can complete a quiz without network access. Submit results when connectivity returns. The nuclear-motd offline message cache pattern applies directly.

**Admin web panel.** The existing Flask admin (your CS50 main branch) is already a fully functional question management interface. Point it at the same nuclear-motd server database (or a dedicated quiz database on the same server) so you can manage categories and questions for the mobile app through the web admin without duplicating tooling.

**Interstitial ad timing.** Show the interstitial after the score is displayed, not before. Apple reviewers and users both react badly to ads that block content. A 2-3 second delay after the score appears feels natural and avoids accidental closes. Cap at once per 3 quiz completions server-side to prevent policy violations.

**Revenue estimate context.** A niche technical audience like nuclear professionals will have lower ad fill rates than consumer apps, but higher CPMs (nuclear/energy industry keywords command premium AdMob rates). The Remove Ads IAP at $2.99 is likely to convert well with this audience — professional users strongly prefer a clean experience. Consider also a "Nuclear Quiz Pro" annual subscription ($9.99/year) that includes Remove Ads plus an expanded question bank, if the question library grows substantially.

**Question bank expansion.** The current schema supports difficulty ratings and source citations. Adding 200–500 questions across CANDU systems, IAEA safety standards, radiation protection, reactor physics, and NOP/GOP/EOP topics would make this genuinely useful for operators studying for certification exams — a strong value proposition for both users and potential employer sponsors.

**Sponsor banner slot.** Nuclear-motd already has sponsor tracking infrastructure (POST /track/sponsor/impression, POST /track/sponsor/click). A dedicated non-AdMob sponsor banner from a nuclear industry vendor (simulator companies, training firms, health physics consultants) would yield significantly higher CPM than AdMob for this audience. This is the nuclear-motd monetization model and it translates directly.

---

## Privacy Policy (Full Text for /quiz/privacy-policy endpoint)

```
Nuclear Quiz — Privacy Policy
Kernkraft Consulting Inc.
Last updated: [DATE]

1. Introduction
Nuclear Quiz ("the App") is operated by Kernkraft Consulting Inc. ("we", "us", "our").
This Privacy Policy explains how we collect, use, and protect your information.

2. Information We Collect
- Account information: email address, username, encrypted password hash
- Quiz activity: questions answered, scores, categories attempted, timestamps
- Device information: device type, OS version, app version (for crash reporting)
- Advertising identifiers: Google Advertising ID / IDFA (used by AdMob for ad targeting)
- Analytics: screen views, feature usage, session duration (Firebase Analytics)
- Crash data: stack traces and device state at time of crash (Firebase Crashlytics)

3. Biometric Data
If you enable biometric login, biometric data (Face ID, fingerprint) is processed
entirely by your device's operating system. We never access, store, or transmit
biometric data.

4. How We Use Your Information
- To provide and operate the App and your account
- To save and display your quiz progress and statistics
- To display advertisements via Google AdMob
- To analyse usage and improve the App
- To diagnose and fix crashes and errors
- To send optional quiz reminder notifications (with your permission)

5. Google AdMob
The App uses Google AdMob to display advertisements. AdMob may use your advertising
identifier and device information to show interest-based ads. You can opt out of
interest-based advertising in your device settings:
  Android: Settings > Google > Ads > Opt out of Ads Personalisation
  iOS: Settings > Privacy > Apple Advertising > Personalised Ads (off)
Google's privacy policy: https://policies.google.com/privacy

6. Firebase
The App uses Google Firebase for analytics and crash reporting. Data is processed
according to Google's privacy policy. Analytics data is aggregated and anonymised.
Crash reports may include device state information but do not include personally
identifiable information beyond device identifiers.

7. In-App Purchases
If you purchase "Remove Ads", your payment is processed by Apple or Google according
to their respective terms. We receive confirmation of the purchase but not payment
details. Purchase records are stored on our server to restore your purchase on new
devices.

8. Data Sharing
We do not sell personal information. We share data only with:
- Google (AdMob, Firebase) — as described above
- Apple / Google Play — for IAP verification
- No other third parties

9. Data Retention
Account data is retained while your account is active. You may request deletion at
any time from the Profile screen or by contacting privacy@nuclear-motd.com.
Firebase analytics data is retained for 14 months per Firebase defaults.

10. Children's Privacy
The App is not directed to children under 13. We do not knowingly collect data from
children under 13. If you believe a child has provided us data, contact us and we
will delete it.

11. Your Rights (GDPR / PIPEDA)
You have the right to access, correct, or delete your personal data. Contact us at
privacy@nuclear-motd.com to exercise these rights.

12. Security
Data is transmitted over HTTPS. Passwords are hashed and never stored in plain text.
Auth tokens are stored in device secure storage.

13. Changes
We may update this policy. The updated date above will reflect changes. Continued
use of the App after changes constitutes acceptance.

14. Contact
privacy@nuclear-motd.com | https://nuclear-motd.com
```

---

## Terms & Conditions (Full Text for /quiz/terms endpoint)

```
Nuclear Quiz — Terms & Conditions
Kernkraft Consulting Inc.
Last updated: [DATE]

1. Acceptance
By downloading or using Nuclear Quiz ("the App"), you agree to these Terms. If you
do not agree, do not use the App.

2. Eligibility
You must be at least 13 years old to use the App. In-app purchases require you to be
18 or older, or have parental consent. By using the App you represent that you meet
these requirements.

3. Account
You are responsible for maintaining the confidentiality of your login credentials.
You may not share your account or create accounts on behalf of others. One account
per person.

4. Educational Purpose & Disclaimer
Quiz content is provided for educational and self-study purposes only. It does not
constitute professional advice, certified training, regulatory guidance, or a
qualification program. Results do not indicate or certify competency for any
regulated nuclear activity. Always follow your organization's procedures and
applicable regulatory requirements.

5. In-App Purchases
"Remove Ads" is a one-time non-refundable purchase that removes advertisements from
your account. Refunds are subject to the policies of the App Store (Apple) or Google
Play from which you made the purchase. Purchases are tied to your Nuclear Quiz
account and can be restored on new devices by logging in.

6. Intellectual Property
All quiz content, questions, branding, code, and materials are the property of
Kernkraft Consulting Inc. You may not reproduce, distribute, or create derivative
works without written permission.

7. Prohibited Use
You may not: reverse engineer the App, use automated tools to scrape questions,
attempt to gain unauthorized access to the server, create accounts with false
information, or use the App for any unlawful purpose.

8. Service Availability
We aim to maintain continuous service but do not guarantee uninterrupted availability.
We reserve the right to modify or discontinue the App at any time.

9. Termination
We may suspend or terminate your account for violation of these Terms, without notice.

10. Limitation of Liability
To the fullest extent permitted by law, Kernkraft Consulting Inc. is not liable for
any indirect, incidental, or consequential damages arising from your use of the App.
Our liability is limited to the amount you paid for the App, if any.

11. Governing Law
These Terms are governed by the laws of the Province of Ontario and the federal laws
of Canada applicable therein, without regard to conflict of law principles.

12. Changes
We may update these Terms. The updated date above reflects changes. Continued use
after changes constitutes acceptance.

13. Contact
Kernkraft Consulting Inc.
privacy@nuclear-motd.com | https://nuclear-motd.com
```

---

## Build & Release Checklist (mirroring nuclear-motd workflow)

- [ ] Create new Firebase project (or add app to existing nuclear-motd Firebase project)
- [ ] Add `google-services.json` (Android) and `GoogleService-Info.plist` (iOS)
- [ ] Create new AdMob app entries for Nuclear Quiz Android and iOS; add ad unit IDs to app_config.dart
- [ ] Register in_app_purchase product IDs in Play Console (one-time) and App Store Connect (non-consumable)
- [ ] Set up Codemagic workflow (copy nuclear-motd codemagic.yaml, update app ID and signing)
- [ ] Generate Android keystore; add to Codemagic environment variables
- [ ] Configure iOS signing in App Store Connect; add to Codemagic
- [ ] Deploy /quiz/* API endpoints on nuclear-motd.com server
- [ ] Deploy /quiz/privacy-policy and /quiz/terms HTML pages
- [ ] Submit Privacy Policy URL and Terms URL in Play Console and App Store Connect
- [ ] Enter AdMob payment info and link app store listings to trigger ad serving
- [ ] Upload to Play Internal Testing track (triggers AdMob activation)
- [ ] Submit iOS build to TestFlight via Codemagic
