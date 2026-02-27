package com.nuclearmotd.quiz.ui.quiz

import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Home
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.nuclearmotd.quiz.UiState
import com.nuclearmotd.quiz.data.api.ResultsResponse
import kotlin.math.roundToInt

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ResultsScreen(
    quizId: String,
    onHome: () -> Unit,
    onReview: () -> Unit, // New callback
    vm: ResultsViewModel = viewModel()
) {
    val resultsState by vm.resultsState.collectAsState()

    LaunchedEffect(quizId) {
        vm.loadResults(quizId)
    }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Results") },
                actions = {
                    IconButton(onClick = onHome) {
                        Icon(Icons.Default.Home, contentDescription = "Home")
                    }
                }
            )
        }
    ) { innerPadding ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding),
            contentAlignment = Alignment.Center
        ) {
            when (val state = resultsState) {
                is UiState.Loading -> CircularProgressIndicator()
                is UiState.Error -> {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Text(state.message, color = MaterialTheme.colorScheme.error)
                        Spacer(Modifier.height(8.dp))
                        Button(onClick = { vm.loadResults(quizId) }) { Text("Retry") }
                    }
                }
                is UiState.Success -> ResultsContent(results = state.data, onHome = onHome, onReview = onReview)
            }
        }
    }
}

@Composable
private fun ResultsContent(results: ResultsResponse, onHome: () -> Unit, onReview: () -> Unit) {
    val percentage = results.percentage.roundToInt()
    val passed = percentage >= 70

    Column(
        modifier = Modifier
            .fillMaxWidth()
            .padding(32.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text(
            text = if (passed) "Well done!" else "Keep practising!",
            style = MaterialTheme.typography.headlineSmall,
            fontWeight = FontWeight.Bold
        )

        Spacer(Modifier.height(24.dp))

        Card(
            colors = CardDefaults.cardColors(
                containerColor = if (passed)
                    MaterialTheme.colorScheme.primaryContainer
                else
                    MaterialTheme.colorScheme.errorContainer
            )
        ) {
            Column(
                modifier = Modifier.padding(32.dp),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                Text(
                    text = "$percentage%",
                    fontSize = 56.sp,
                    fontWeight = FontWeight.Bold,
                    color = if (passed)
                        MaterialTheme.colorScheme.onPrimaryContainer
                    else
                        MaterialTheme.colorScheme.onErrorContainer
                )
                Text(
                    text = "${results.score} / ${results.totalQuestions} correct",
                    style = MaterialTheme.typography.bodyLarge,
                    color = if (passed)
                        MaterialTheme.colorScheme.onPrimaryContainer
                    else
                        MaterialTheme.colorScheme.onErrorContainer
                )
            }
        }

        results.category?.let {
            Spacer(Modifier.height(16.dp))
            Text(
                text = "Category: $it",
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.7f),
                textAlign = TextAlign.Center
            )
        }

        Spacer(Modifier.height(32.dp))

        Button(
            onClick = onReview,
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Review Answers")
        }

        Spacer(Modifier.height(8.dp))

        OutlinedButton(
            onClick = onHome,
            modifier = Modifier.fillMaxWidth()
        ) {
            Text("Back to Home")
        }
    }
}
