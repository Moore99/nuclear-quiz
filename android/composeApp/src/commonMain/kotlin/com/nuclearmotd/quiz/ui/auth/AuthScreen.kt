package com.nuclearmotd.quiz.ui.auth

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.material3.*
import androidx.compose.material3.TabRowDefaults.SecondaryIndicator
import androidx.compose.material3.TabRowDefaults.tabIndicatorOffset
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.input.ImeAction
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.input.PasswordVisualTransformation
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.nuclearmotd.quiz.UiState

@Composable
fun AuthScreen(
    onAuthSuccess: () -> Unit,
    onForgotPassword: () -> Unit,
    vm: AuthViewModel = viewModel()
) {
    val authState by vm.authState.collectAsState()
    var selectedTab by remember { mutableIntStateOf(0) }

    LaunchedEffect(authState) {
        if (authState is UiState.Success) {
            onAuthSuccess()
            vm.resetAuthState()
        }
    }

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(24.dp),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Spacer(Modifier.height(48.dp))

        Text(
            text = "☢ Nuclear Quiz",
            fontSize = 28.sp,
            fontWeight = FontWeight.Bold,
            color = MaterialTheme.colorScheme.primary
        )
        Text(
            text = "Test your nuclear knowledge",
            style = MaterialTheme.typography.bodyMedium,
            color = MaterialTheme.colorScheme.onSurface.copy(alpha = 0.6f)
        )

        Spacer(Modifier.height(40.dp))

        TabRow(
            selectedTabIndex = selectedTab,
            indicator = { tabPositions ->
                SecondaryIndicator(Modifier.tabIndicatorOffset(tabPositions[selectedTab]))
            }
        ) {
            Tab(selected = selectedTab == 0, onClick = { selectedTab = 0; vm.resetAuthState() }) {
                Text("Login", modifier = Modifier.padding(12.dp))
            }
            Tab(selected = selectedTab == 1, onClick = { selectedTab = 1; vm.resetAuthState() }) {
                Text("Register", modifier = Modifier.padding(12.dp))
            }
        }

        Spacer(Modifier.height(24.dp))

        if (selectedTab == 0) {
            LoginForm(
                isLoading = authState is UiState.Loading,
                errorMessage = (authState as? UiState.Error)?.message,
                onLogin = { u, p -> vm.login(u, p) },
                onForgotPassword = onForgotPassword
            )
        } else {
            RegisterForm(
                isLoading = authState is UiState.Loading,
                errorMessage = (authState as? UiState.Error)?.message,
                onRegister = { u, p -> vm.register(u, p) }
            )
        }
    }
}

@Composable
private fun LoginForm(
    isLoading: Boolean,
    errorMessage: String?,
    onLogin: (String, String) -> Unit,
    onForgotPassword: () -> Unit
) {
    var username by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }

    AuthFields(
        username = username,
        password = password,
        onUsernameChange = { username = it },
        onPasswordChange = { password = it },
        errorMessage = errorMessage
    )

    Spacer(Modifier.height(8.dp))
    
    Box(modifier = Modifier.fillMaxWidth(), contentAlignment = Alignment.CenterEnd) {
        TextButton(
            onClick = onForgotPassword
        ) {
            Text("Forgot Password?")
        }
    }

    Spacer(Modifier.height(8.dp))

    Button(
        onClick = { onLogin(username, password) },
        enabled = !isLoading && username.isNotBlank() && password.isNotBlank(),
        modifier = Modifier.fillMaxWidth()
    ) {
        if (isLoading) {
            CircularProgressIndicator(
                modifier = Modifier.size(20.dp),
                strokeWidth = 2.dp,
                color = MaterialTheme.colorScheme.onPrimary
            )
        } else {
            Text("Login")
        }
    }
}

@Composable
private fun RegisterForm(
    isLoading: Boolean,
    errorMessage: String?,
    onRegister: (String, String) -> Unit
) {
    var username by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    var confirmPassword by remember { mutableStateOf("") }
    val passwordMismatch = confirmPassword.isNotEmpty() && password != confirmPassword

    AuthFields(
        username = username,
        password = password,
        onUsernameChange = { username = it },
        onPasswordChange = { password = it },
        errorMessage = errorMessage
    )

    Spacer(Modifier.height(8.dp))

    OutlinedTextField(
        value = confirmPassword,
        onValueChange = { confirmPassword = it },
        label = { Text("Confirm Password") },
        visualTransformation = PasswordVisualTransformation(),
        keyboardOptions = KeyboardOptions(
            keyboardType = KeyboardType.Password,
            autoCorrectEnabled = false,
            imeAction = ImeAction.Done
        ),
        isError = passwordMismatch,
        supportingText = if (passwordMismatch) {
            { Text("Passwords do not match") }
        } else null,
        modifier = Modifier.fillMaxWidth()
    )

    Spacer(Modifier.height(16.dp))

    Button(
        onClick = { onRegister(username, password) },
        enabled = !isLoading && username.isNotBlank() && password.isNotBlank() && !passwordMismatch,
        modifier = Modifier.fillMaxWidth()
    ) {
        if (isLoading) {
            CircularProgressIndicator(
                modifier = Modifier.size(20.dp),
                strokeWidth = 2.dp,
                color = MaterialTheme.colorScheme.onPrimary
            )
        } else {
            Text("Create Account")
        }
    }
}

@Composable
private fun AuthFields(
    username: String,
    password: String,
    onUsernameChange: (String) -> Unit,
    onPasswordChange: (String) -> Unit,
    errorMessage: String?
) {
    OutlinedTextField(
        value = username,
        onValueChange = onUsernameChange,
        label = { Text("Username") },
        singleLine = true,
        keyboardOptions = KeyboardOptions(
            autoCorrectEnabled = false,
            imeAction = ImeAction.Next
        ),
        modifier = Modifier.fillMaxWidth()
    )

    Spacer(Modifier.height(8.dp))

    OutlinedTextField(
        value = password,
        onValueChange = onPasswordChange,
        label = { Text("Password") },
        visualTransformation = PasswordVisualTransformation(),
        keyboardOptions = KeyboardOptions(
            keyboardType = KeyboardType.Password,
            autoCorrectEnabled = false,
            imeAction = ImeAction.Next
        ),
        singleLine = true,
        modifier = Modifier.fillMaxWidth()
    )

    if (errorMessage != null) {
        Spacer(Modifier.height(8.dp))
        Text(
            text = errorMessage,
            color = MaterialTheme.colorScheme.error,
            style = MaterialTheme.typography.bodySmall
        )
    }
}
