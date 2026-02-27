package com.nuclearmotd.quiz.ui.quiz

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.nuclearmotd.quiz.UiState
import com.nuclearmotd.quiz.data.api.ReviewItem

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ReviewScreen(
    quizId: String,
    onBack: () -> Unit,
    vm: ResultsViewModel = viewModel()
) {
    val resultsState by vm.resultsState.collectAsState()

    LaunchedEffect(quizId) {
        vm.loadResults(quizId)
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Review Answers") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                }
            )
        }
    ) { innerPadding ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
        ) {
            when (val state = resultsState) {
                is UiState.Loading -> CircularProgressIndicator(Modifier.align(Alignment.Center))
                is UiState.Error -> Text(state.message, modifier = Modifier.align(Alignment.Center))
                is UiState.Success -> {
                    val reviewList = state.data.review ?: emptyList()
                    if (reviewList.isEmpty()) {
                        Text("No review data available", modifier = Modifier.align(Alignment.Center))
                    } else {
                        LazyColumn(
                            modifier = Modifier.fillMaxSize(),
                            contentPadding = PaddingValues(16.dp),
                            verticalArrangement = Arrangement.spacedBy(16.dp)
                        ) {
                            items(reviewList) { item ->
                                ReviewCard(item)
                            }
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun ReviewCard(item: ReviewItem) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(
            containerColor = if (item.isCorrect) 
                MaterialTheme.colorScheme.primaryContainer.copy(alpha = 0.3f)
            else 
                MaterialTheme.colorScheme.errorContainer.copy(alpha = 0.3f)
        )
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(
                text = item.questionText,
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold
            )
            Spacer(Modifier.height(8.dp))
            
            Text(text = "Your Answer:", style = MaterialTheme.typography.labelSmall)
            Text(
                text = item.userAnswer,
                style = MaterialTheme.typography.bodyMedium,
                color = if (item.isCorrect) 
                    MaterialTheme.colorScheme.primary 
                else 
                    MaterialTheme.colorScheme.error
            )
            
            if (!item.isCorrect) {
                Spacer(Modifier.height(8.dp))
                Text(text = "Correct Answer:", style = MaterialTheme.typography.labelSmall)
                Text(
                    text = item.correctAnswer,
                    style = MaterialTheme.typography.bodyMedium,
                    fontWeight = FontWeight.SemiBold
                )
            }
            
            item.explanation?.let {
                Spacer(Modifier.height(12.dp))
                Text(text = "Explanation:", style = MaterialTheme.typography.labelSmall)
                Text(text = it, style = MaterialTheme.typography.bodySmall)
            }
            
            item.source?.let {
                Spacer(Modifier.height(4.dp))
                Text(
                    text = "Source: $it",
                    style = MaterialTheme.typography.labelSmall,
                    color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.5f)
                )
            }
        }
    }
}
