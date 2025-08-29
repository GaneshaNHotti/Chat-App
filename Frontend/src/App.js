import { Switch, Route } from "wouter";
import { queryClient } from "./lib/queryClient";
import { QueryClientProvider } from "@tanstack/react-query";
import { useAuth } from "./cpmponents/hooks/useAuth";
import LoginForm from "./components/login-form";
import NotFound from "./components/not-found";

function Router() {
  const { isAuthenticated, isLoading } = useAuth();

  return (
    <Switch>
      {isLoading || !isAuthenticated ? (
        <Route path="/" component={LoginForm} />
      ) : (
        <Route component={NotFound} />
      )}
    </Switch>
  );
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
        <Router />
    </QueryClientProvider>
  );
}

export default App;
