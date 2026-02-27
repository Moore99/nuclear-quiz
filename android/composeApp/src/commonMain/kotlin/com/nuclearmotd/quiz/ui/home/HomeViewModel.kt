package com.nuclearmotd.quiz.ui.home

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.nuclearmotd.quiz.AppDependencies
import com.nuclearmotd.quiz.UiState
import com.nuclearmotd.quiz.data.api.ApiException
import com.nuclearmotd.quiz.data.api.Category
import com.nuclearmotd.quiz.data.api.StartQuizRequest
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

class HomeViewModel : ViewModel() {

    private val api = AppDependencies.api

    private val _categories = MutableStateFlow<UiState<List<Category>>>(UiState.Loading)
    val categories: StateFlow<UiState<List<Category>>> = _categories

    private val _startQuizState = MutableStateFlow<UiState<String>?>(null)
    val startQuizState: StateFlow<UiState<String>?> = _startQuizState

    val username: String get() = AppDependencies.tokenStore.getUsername() ?: "User"

    init {
        loadCategories()
    }

    fun loadCategories() {
        _categories.value = UiState.Loading
        viewModelScope.launch {
            try {
                _categories.value = UiState.Success(api.getCategories())
            } catch (e: ApiException) {
                _categories.value = UiState.Error("Failed to load categories (${e.statusCode})")
            } catch (e: Exception) {
                _categories.value = UiState.Error("Network error: ${e.message}")
            }
        }
    }

    fun startQuiz(categoryId: Int?) {
        _startQuizState.value = UiState.Loading
        viewModelScope.launch {
            try {
                // If categoryId is null (Random Quiz), try to pick a random category ID from loaded ones
                // because the server seems to require category_id.
                val actualCategoryId = categoryId ?: (categories.value as? UiState.Success)?.data?.randomOrNull()?.id
                
                val response = api.startQuiz(StartQuizRequest(categoryId = actualCategoryId))
                _startQuizState.value = UiState.Success(response.quizId)
            } catch (e: ApiException) {
                _startQuizState.value = UiState.Error("Failed to start quiz (${e.statusCode})")
            } catch (e: Exception) {
                _startQuizState.value = UiState.Error("Network error: ${e.message}")
            }
        }
    }

    fun resetStartState() {
        _startQuizState.value = null
    }

    fun logout() {
        AppDependencies.tokenStore.clear()
    }
}
