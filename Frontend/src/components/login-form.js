import { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import {
  Button,
  TextField,
  Typography,
  Container,
  Box,
  CircularProgress,
  Snackbar,
  Alert,
} from "@mui/material";
import { apiRequest } from "../lib/queryClient";

export default function LoginForm() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [isSignUp, setIsSignUp] = useState(false);

  // Snackbar state
  const [toast, setToast] = useState({
    open: false,
    message: "",
    severity: "success",
  });

  const queryClient = useQueryClient();

  const loginMutation = useMutation({
    mutationFn: async (credentials) => {
      const endpoint = isSignUp ? "/api/auth/signup" : "/api/auth/login";
      const response = await apiRequest("POST", endpoint, credentials);
      if (!response.ok) {
        const err = await response.json();
        throw new Error(err.message || "Authentication failed");
      }
      return response.json();
    },
    onSuccess: () => {
      setToast({
        open: true,
        message: isSignUp
          ? "Account created successfully!"
          : "Logged in successfully!",
        severity: "success",
      });
      queryClient.invalidateQueries({ queryKey: ["/api/auth/user"] });
    },
    onError: (error) => {
      setToast({
        open: true,
        message: error.message || "Authentication failed",
        severity: "error",
      });
    },
  });

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!username.trim()) {
      setToast({
        open: true,
        message: "Username is required",
        severity: "error",
      });
      return;
    }

    if (isSignUp && !email.trim()) {
      setToast({
        open: true,
        message: "Email is required for sign up",
        severity: "error",
      });
      return;
    }

    loginMutation.mutate({
      username: username.trim(),
      ...(isSignUp && { email: email.trim() }),
    });
  };

  return (
    <Container maxWidth="xs">
      <Box
        sx={{
          mt: 8,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        <Typography component="h1" variant="h5">
          {isSignUp ? "Create Account" : "Sign In"}
        </Typography>
        <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
          {isSignUp ? "Join the chat community" : "Welcome back to the chat"}
        </Typography>

        <Box component="form" onSubmit={handleSubmit} sx={{ mt: 3 }}>
          <TextField
            margin="normal"
            required
            fullWidth
            id="username"
            label="Username"
            name="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />

          {isSignUp && (
            <TextField
              margin="normal"
              required
              fullWidth
              id="email"
              label="Email Address"
              name="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          )}

          <Button
            type="submit"
            fullWidth
            variant="contained"
            disabled={loginMutation.isPending}
            sx={{ mt: 3, mb: 2 }}
          >
            {loginMutation.isPending ? (
              <>
                <CircularProgress size={20} sx={{ mr: 1 }} />
                {isSignUp ? "Creating Account..." : "Signing In..."}
              </>
            ) : isSignUp ? (
              "Create Account"
            ) : (
              "Sign In"
            )}
          </Button>

          <Button
            type="button"
            fullWidth
            variant="text"
            onClick={() => {
              setIsSignUp(!isSignUp);
              setEmail("");
            }}
          >
            {isSignUp
              ? "Already have an account? Sign In"
              : "Need an account? Sign Up"}
          </Button>
        </Box>
      </Box>

      {/* Snackbar Toast */}
      <Snackbar
        open={toast.open}
        autoHideDuration={4000}
        onClose={() => setToast((prev) => ({ ...prev, open: false }))}
        anchorOrigin={{ vertical: "top", horizontal: "center" }}
      >
        <Alert
          onClose={() => setToast((prev) => ({ ...prev, open: false }))}
          severity={toast.severity}
          sx={{ width: "100%" }}
        >
          {toast.message}
        </Alert>
      </Snackbar>
    </Container>
  );
}
