package com.nuclearmotd.quiz.ui.quiz

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.nuclearmotd.quiz.AppDependencies
import com.nuclearmotd.quiz.UiState
import com.nuclearmotd.quiz.data.api.ApiException
import com.nuclearmotd.quiz.data.api.ResultsResponse
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

class ResultsViewModel : ViewModel() {

    private val api = AppDependencies.api

    private val _resultsState = MutableStateFlow<UiState<ResultsResponse>>(UiState.Loading)
    val resultsState: StateFlow<UiState<ResultsResponse>> = _resultsState

    fun loadResults(quizId: String) { // Changed from Int to String
        _resultsState.value = UiState.Loading
        viewModelScope.launch {
            try {
                _resultsState.value = UiState.Success(api.getResults(quizId))
            } catch (e: ApiException) {
                _resultsState.value = UiState.Error("Failed to load results (${e.statusCode})")
            } catch (e: Exception) {
                _resultsState.value = UiState.Error("Network error: ${e.message}")
            }
        }
    }
}
