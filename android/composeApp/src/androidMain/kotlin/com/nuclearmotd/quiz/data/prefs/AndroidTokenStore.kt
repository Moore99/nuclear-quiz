package com.nuclearmotd.quiz.data.prefs

import android.content.Context
import androidx.security.crypto.EncryptedSharedPreferences
import androidx.security.crypto.MasterKey

class AndroidTokenStore(context: Context) : TokenStore {

    private val masterKey = MasterKey.Builder(context)
        .setKeyScheme(MasterKey.KeyScheme.AES256_GCM)
        .build()

    private val prefs = EncryptedSharedPreferences.create(
        context,
        "nuclear_quiz_prefs",
        masterKey,
        EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
        EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM
    )

    override fun saveToken(token: String, username: String, userId: Int) {
        prefs.edit()
            .putString(KEY_TOKEN, token)
            .putString(KEY_USERNAME, username)
            .putInt(KEY_USER_ID, userId)
            .apply()
    }

    override fun getToken(): String? = prefs.getString(KEY_TOKEN, null)

    override fun getUsername(): String? = prefs.getString(KEY_USERNAME, null)

    override fun getUserId(): Int = prefs.getInt(KEY_USER_ID, -1)

    override fun isLoggedIn(): Boolean = getToken() != null

    override fun clear() {
        prefs.edit().clear().apply()
    }

    companion object {
        private const val KEY_TOKEN = "auth_token"
        private const val KEY_USERNAME = "username"
        private const val KEY_USER_ID = "user_id"
    }
}
