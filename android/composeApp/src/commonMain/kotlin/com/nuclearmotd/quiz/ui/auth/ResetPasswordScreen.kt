package com.nuclearmotd.quiz.ui.auth

import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.nuclearmotd.quiz.UiState

/**
 * Forgot-password screen — submits a username and triggers a server-side reset email.
 * The user then clicks the link in the email to set a new password via the web UI.
 */
@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun ResetPasswordScreen(
    onBack: () -> Unit,
    onSuccess: () -> Unit,
    vm: AuthViewModel = viewModel()
) {
    val forgotState by vm.forgotState.collectAsState()
    var username by remember { mutableStateOf("") }

    LaunchedEffect(forgotState) {
        if (forgotState is UiState.Success) onSuccess()
    }

    DisposableEffect(Unit) { onDispose { vm.resetForgotState() } }

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("Forgot Password") },
                navigationIcon = {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back")
                    }
                }
            )
        }
    ) { innerPadding ->
        Column(
            modifier = Modifier
                .fillMaxSize()
                .padding(innerPadding)
                .padding(32.dp),
            horizontalAlignment = Alignment.CenterHorizontally,
            verticalArrangement = Arrangement.Center
        ) {
            Text(
                text = "Enter your username. If an account exists, we'll send a password reset link to the registered email.",
                style = MaterialTheme.typography.bodyMedium,
                textAlign = TextAlign.Center,
                modifier = Modifier.padding(bottom = 24.dp)
            )

            OutlinedTextField(
                value = username,
                onValueChange = { username = it },
                label = { Text("Username") },
                singleLine = true,
                modifier = Modifier.fillMaxWidth()
            )

            Spacer(Modifier.height(24.dp))

            Button(
                onClick = { vm.forgotPassword(username) },
                modifier = Modifier.fillMaxWidth(),
                enabled = forgotState !is UiState.Loading && username.isNotBlank()
            ) {
                if (forgotState is UiState.Loading) {
                    CircularProgressIndicator(modifier = Modifier.size(20.dp), strokeWidth = 2.dp)
                } else {
                    Text("Send Reset Link")
                }
            }

            if (forgotState is UiState.Error) {
                Text(
                    text = (forgotState as UiState.Error).message,
                    color = MaterialTheme.colorScheme.error,
                    modifier = Modifier.padding(top = 8.dp)
                )
            }
        }
    }
}
