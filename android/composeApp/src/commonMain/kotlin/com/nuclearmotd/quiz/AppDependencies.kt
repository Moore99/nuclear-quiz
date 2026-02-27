package com.nuclearmotd.quiz

import com.nuclearmotd.quiz.data.api.QuizApi
import com.nuclearmotd.quiz.data.api.createHttpClient
import com.nuclearmotd.quiz.data.prefs.TokenStore

object AppDependencies {
    private lateinit var _tokenStore: TokenStore
    private lateinit var _api: QuizApi

    fun init(tokenStore: TokenStore) {
        if (::_tokenStore.isInitialized) return
        _tokenStore = tokenStore
        _api = QuizApi(createHttpClient(tokenStore))
    }

    val tokenStore: TokenStore get() = _tokenStore
    val api: QuizApi get() = _api
}
