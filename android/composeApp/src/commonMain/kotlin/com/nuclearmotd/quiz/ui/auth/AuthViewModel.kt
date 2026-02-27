package com.nuclearmotd.quiz.ui.auth

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.nuclearmotd.quiz.AppDependencies
import com.nuclearmotd.quiz.UiState
import com.nuclearmotd.quiz.data.api.ApiException
import com.nuclearmotd.quiz.data.api.LoginRequest
import com.nuclearmotd.quiz.data.api.RegisterRequest
import com.nuclearmotd.quiz.data.api.ResetPasswordRequest
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

class AuthViewModel : ViewModel() {

    private val api = AppDependencies.api
    private val tokenStore = AppDependencies.tokenStore

    private val _authState = MutableStateFlow<UiState<Unit>?>(null)
    val authState: StateFlow<UiState<Unit>?> = _authState

    private val _resetState = MutableStateFlow<UiState<Unit>?>(null)
    val resetState: StateFlow<UiState<Unit>?> = _resetState

    fun login(username: String, password: String) {
        _authState.value = UiState.Loading
        viewModelScope.launch {
            try {
                val trimmedUsername = username.trim()
                val body = api.login(LoginRequest(trimmedUsername, password.trim()))
                tokenStore.saveToken(body.token, body.username ?: trimmedUsername, body.userId)
                _authState.value = UiState.Success(Unit)
            } catch (e: ApiException) {
                val msg = when (e.statusCode) {
                    401 -> "Invalid username or password"
                    else -> "Login failed (${e.statusCode})"
                }
                _authState.value = UiState.Error(msg)
            } catch (e: Exception) {
                _authState.value = UiState.Error("Network error: ${e.message}")
            }
        }
    }

    fun register(username: String, password: String) {
        _authState.value = UiState.Loading
        viewModelScope.launch {
            try {
                val trimmedUsername = username.trim()
                val body = api.register(RegisterRequest(trimmedUsername, password.trim()))
                tokenStore.saveToken(body.token, body.username ?: trimmedUsername, body.userId)
                _authState.value = UiState.Success(Unit)
            } catch (e: ApiException) {
                val msg = when (e.statusCode) {
                    409 -> "Username already taken"
                    400 -> "Invalid username or password"
                    else -> "Registration failed (${e.statusCode})"
                }
                _authState.value = UiState.Error(msg)
            } catch (e: Exception) {
                _authState.value = UiState.Error("Network error: ${e.message}")
            }
        }
    }

    fun resetPassword(username: String, newPassword: String) {
        _resetState.value = UiState.Loading
        viewModelScope.launch {
            try {
                api.resetPassword(ResetPasswordRequest(username.trim(), newPassword.trim()))
                _resetState.value = UiState.Success(Unit)
            } catch (e: ApiException) {
                _resetState.value = UiState.Error("Failed to reset password (${e.statusCode})")
            } catch (e: Exception) {
                _resetState.value = UiState.Error("Network error: ${e.message}")
            }
        }
    }

    fun resetAuthState() {
        _authState.value = null
    }

    fun resetResetState() {
        _resetState.value = null
    }
}
