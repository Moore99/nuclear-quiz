# Nuclear Quiz — Development Branch

> **Note**: This file previously contained plans for a Flutter app that was never built.
> The mobile app is **Compose Multiplatform (Kotlin/KMP)**, not Flutter.
> See `CLAUDE.md` for accurate project documentation.

## Mobile App

The mobile app lives in `android/` and uses Compose Multiplatform (CMP) to target both Android and iOS from a single Kotlin codebase.

- **Framework**: Compose Multiplatform (CMP) 1.7.3, Kotlin 2.0.21
- **Networking**: Ktor 3.0.3
- **Architecture**: MVVM, StateFlow, `AppDependencies` singleton
- **Navigation**: Type-safe nav (`@Serializable` route objects)
- **Token storage**: `TokenStore` interface; `AndroidTokenStore` (EncryptedSharedPreferences); `IosTokenStore` (NSUserDefaults — Keychain needed for production)

## Running the App

**Android:**
```
Open android/ in Android Studio → Gradle sync → Run
```

**iOS framework verification:**
```bash
cd android
./gradlew :composeApp:linkDebugFrameworkIosSimulatorArm64
```
Then open `android/iosApp/iosApp.xcodeproj` in Xcode.

## Roadmap (open items)

- Password reset via email (endpoint removed pending proper token/email flow)
- iOS Keychain-backed token storage
- AdMob integration
- Firebase Analytics + Crashlytics
- In-app purchase (Remove Ads)
- Privacy policy + terms pages at `/quiz/privacy-policy` and `/quiz/terms`
- Database backup endpoint (`/admin/backup`)

For full context, read `CLAUDE.md`.
