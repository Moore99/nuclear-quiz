package com.nuclearmotd.quiz.data.prefs

interface TokenStore {
    fun saveToken(token: String, username: String, userId: Int)
    fun getToken(): String?
    fun getUsername(): String?
    fun getUserId(): Int
    fun isLoggedIn(): Boolean
    fun clear()
}
