package com.nuclearmotd.quiz.ui.auth

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.nuclearmotd.quiz.AppDependencies
import com.nuclearmotd.quiz.UiState
import com.nuclearmotd.quiz.data.api.ApiException
import com.nuclearmotd.quiz.data.api.ChangePasswordRequest
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

class AccountViewModel : ViewModel() {

    private val api = AppDependencies.api

    private val _accountState = MutableStateFlow<UiState<String>?>(null)
    val accountState: StateFlow<UiState<String>?> = _accountState

    fun changePassword(current: String, new: String) {
        _accountState.value = UiState.Loading
        viewModelScope.launch {
            try {
                api.changePassword(ChangePasswordRequest(current.trim(), new.trim()))
                _accountState.value = UiState.Success("password_changed")
            } catch (e: ApiException) {
                _accountState.value = UiState.Error("Failed to change password (${e.statusCode})")
            } catch (e: Exception) {
                _accountState.value = UiState.Error("Network error: ${e.message}")
            }
        }
    }

    fun deleteAccount() {
        _accountState.value = UiState.Loading
        viewModelScope.launch {
            try {
                api.deleteAccount()
                _accountState.value = UiState.Success("deleted")
            } catch (e: ApiException) {
                _accountState.value = UiState.Error("Failed to delete account (${e.statusCode})")
            } catch (e: Exception) {
                _accountState.value = UiState.Error("Network error: ${e.message}")
            }
        }
    }

    fun resetState() {
        _accountState.value = null
    }
}
