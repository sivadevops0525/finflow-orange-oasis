import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { SidebarProvider } from "@shared/components/ui/sidebar";
import { AppSidebar } from "./components/AppSidebar";
import { MicrofrontendLoader } from "./components/MicrofrontendLoader";
import { Toaster } from "@shared/components/ui/toaster";
import { Toaster as Sonner } from "@shared/components/ui/sonner";
import { TooltipProvider } from "@shared/components/ui/tooltip";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import "./index.css";

const queryClient = new QueryClient();

const App = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <TooltipProvider>
        <Toaster />
        <Sonner />
        <BrowserRouter>
          <SidebarProvider>
            <div className="min-h-screen flex w-full bg-gradient-to-br from-orange-50 to-white">
              <AppSidebar />
              <main className="flex-1 overflow-hidden">
                <Routes>
                  <Route path="/" element={<Navigate to="/dashboard" replace />} />
                  <Route 
                    path="/dashboard" 
                    element={
                      <MicrofrontendLoader 
                        name="dashboard" 
                        url={import.meta.env.VITE_DASHBOARD_URL || "http://localhost:3001"} 
                      />
                    } 
                  />
                  <Route 
                    path="/expenses" 
                    element={
                      <MicrofrontendLoader 
                        name="expenses" 
                        url={import.meta.env.VITE_EXPENSES_URL || "http://localhost:3002"} 
                      />
                    } 
                  />
                  <Route 
                    path="/income" 
                    element={
                      <MicrofrontendLoader 
                        name="income" 
                        url={import.meta.env.VITE_INCOME_URL || "http://localhost:3003"} 
                      />
                    } 
                  />
                  <Route 
                    path="/budget" 
                    element={
                      <MicrofrontendLoader 
                        name="budget" 
                        url={import.meta.env.VITE_BUDGET_URL || "http://localhost:3004"} 
                      />
                    } 
                  />
                  <Route 
                    path="/wishlist" 
                    element={
                      <MicrofrontendLoader 
                        name="wishlist" 
                        url={import.meta.env.VITE_WISHLIST_URL || "http://localhost:3005"} 
                      />
                    } 
                  />
                  <Route 
                    path="/reports" 
                    element={
                      <MicrofrontendLoader 
                        name="reports" 
                        url={import.meta.env.VITE_REPORTS_URL || "http://localhost:3006"} 
                      />
                    } 
                  />
                </Routes>
              </main>
            </div>
          </SidebarProvider>
        </BrowserRouter>
      </TooltipProvider>
    </QueryClientProvider>
  );
};

export default App;