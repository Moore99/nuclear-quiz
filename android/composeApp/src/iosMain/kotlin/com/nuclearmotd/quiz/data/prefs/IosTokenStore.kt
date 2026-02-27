package com.nuclearmotd.quiz.data.prefs

import platform.Foundation.NSUserDefaults

/**
 * iOS token storage backed by NSUserDefaults.
 * NOTE: For production, replace with Keychain storage for security.
 */
class IosTokenStore : TokenStore {

    private val defaults = NSUserDefaults.standardUserDefaults

    override fun saveToken(token: String, username: String, userId: Int) {
        defaults.setObject(token, KEY_TOKEN)
        defaults.setObject(username, KEY_USERNAME)
        defaults.setInteger(userId.toLong(), KEY_USER_ID)
        defaults.synchronize()
    }

    override fun getToken(): String? =
        defaults.stringForKey(KEY_TOKEN)

    override fun getUsername(): String? =
        defaults.stringForKey(KEY_USERNAME)

    override fun getUserId(): Int =
        defaults.integerForKey(KEY_USER_ID).toInt()

    override fun isLoggedIn(): Boolean = getToken() != null

    override fun clear() {
        defaults.removeObjectForKey(KEY_TOKEN)
        defaults.removeObjectForKey(KEY_USERNAME)
        defaults.removeObjectForKey(KEY_USER_ID)
        defaults.synchronize()
    }

    companion object {
        private const val KEY_TOKEN = "auth_token"
        private const val KEY_USERNAME = "username"
        private const val KEY_USER_ID = "user_id"
    }
}
