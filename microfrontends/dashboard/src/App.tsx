import { useState, useEffect } from "react";
import { PageHeader } from "@shared/components/layout/PageHeader";
import { Card, CardContent, CardHeader, CardTitle } from "@shared/components/ui/card";
import { Progress } from "@shared/components/ui/progress";
import {
  DollarSign,
  TrendingUp,
  TrendingDown,
  PiggyBank,
  Target,
  Calendar,
  ArrowUpIcon,
  ArrowDownIcon
} from "lucide-react";
import { LineChart, Line, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from "recharts";
import "./index.css";

const Dashboard = () => {
  const [stats, setStats] = useState({
    totalIncome: 0,
    totalExpenses: 0,
    currentSavings: 0,
    budgetUtilization: 0
  });

  const [recentTransactions, setRecentTransactions] = useState([]);
  const [budgetData, setBudgetData] = useState([]);

  // Mock data for charts
  const monthlyData = [
    { month: 'Jan', income: 4500, expenses: 3200, savings: 1300 },
    { month: 'Feb', income: 4200, expenses: 3100, savings: 1100 },
    { month: 'Mar', income: 4800, expenses: 3400, savings: 1400 },
    { month: 'Apr', income: 4600, expenses: 3300, savings: 1300 },
    { month: 'May', income: 5000, expenses: 3600, savings: 1400 },
    { month: 'Jun', income: 4900, expenses: 3500, savings: 1400 },
  ];

  const categoryData = [
    { name: 'Housing', value: 1200, color: '#FF6B35' },
    { name: 'Food', value: 800, color: '#F7931E' },
    { name: 'Transportation', value: 400, color: '#FFB800' },
    { name: 'Entertainment', value: 300, color: '#F16821' },
    { name: 'Utilities', value: 250, color: '#FF8A65' },
  ];

  useEffect(() => {
    // Calculate overview stats
    const totalIncome = monthlyData[monthlyData.length - 1]?.income || 0;
    const totalExpenses = monthlyData[monthlyData.length - 1]?.expenses || 0;
    const currentSavings = totalIncome - totalExpenses;
    const budgetUtilization = (totalExpenses / totalIncome) * 100;

    setStats({
      totalIncome,
      totalExpenses,
      currentSavings,
      budgetUtilization
    });

    // Mock recent transactions
    setRecentTransactions([
      { id: 1, description: "Grocery Store", amount: -85.50, category: "Food", date: "Today" },
      { id: 2, description: "Salary Deposit", amount: 2500.00, category: "Income", date: "Yesterday" },
      { id: 3, description: "Netflix", amount: -12.99, category: "Entertainment", date: "2 days ago" },
      { id: 4, description: "Gas Station", amount: -45.20, category: "Transportation", date: "3 days ago" },
    ]);

    // Mock budget data
    setBudgetData([
      { category: "Housing", spent: 1200, budget: 1500, percentage: 80 },
      { category: "Food", spent: 620, budget: 800, percentage: 77.5 },
      { category: "Transportation", spent: 340, budget: 400, percentage: 85 },
    ]);
  }, []);

  return (
    <div className="flex-1 space-y-6 p-6 pt-0">
      <PageHeader
        title="Dashboard"
        description="Overview of your financial status"
      />

      {/* Stats Cards */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        <Card className="glass-card hover-lift animate-fade-in">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Income</CardTitle>
            <div className="gradient-orange p-2 rounded-lg">
              <TrendingUp className="h-4 w-4 text-white" />
            </div>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-success">${stats.totalIncome.toLocaleString()}</div>
            <div className="flex items-center text-xs text-success">
              <ArrowUpIcon className="mr-1 h-3 w-3" />
              +12% from last month
            </div>
          </CardContent>
        </Card>

        <Card className="glass-card hover-lift animate-fade-in" style={{ animationDelay: '0.1s' }}>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Expenses</CardTitle>
            <div className="gradient-orange p-2 rounded-lg">
              <TrendingDown className="h-4 w-4 text-white" />
            </div>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-destructive">${stats.totalExpenses.toLocaleString()}</div>
            <div className="flex items-center text-xs text-destructive">
              <ArrowDownIcon className="mr-1 h-3 w-3" />
              -3% from last month
            </div>
          </CardContent>
        </Card>

        <Card className="glass-card hover-lift animate-fade-in" style={{ animationDelay: '0.2s' }}>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Current Savings</CardTitle>
            <div className="gradient-orange p-2 rounded-lg">
              <PiggyBank className="h-4 w-4 text-white" />
            </div>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-primary">${stats.currentSavings.toLocaleString()}</div>
            <div className="flex items-center text-xs text-success">
              <ArrowUpIcon className="mr-1 h-3 w-3" />
              +18% from last month
            </div>
          </CardContent>
        </Card>

        <Card className="glass-card hover-lift animate-fade-in" style={{ animationDelay: '0.3s' }}>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Savings Rate</CardTitle>
            <div className="gradient-orange p-2 rounded-lg">
              <Target className="h-4 w-4 text-white" />
            </div>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-primary">{(100 - stats.budgetUtilization).toFixed(1)}%</div>
            <Progress value={100 - stats.budgetUtilization} className="mt-2" />
          </CardContent>
        </Card>
      </div>

      {/* Charts Section */}
      <div className="grid gap-6 md:grid-cols-2">
        <Card className="glass-card animate-fade-in" style={{ animationDelay: '0.4s' }}>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Calendar className="h-5 w-5 text-primary" />
              Income vs Expenses Trend
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={monthlyData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
                <XAxis dataKey="month" stroke="#666" />
                <YAxis stroke="#666" />
                <Tooltip 
                  contentStyle={{ 
                    backgroundColor: 'white', 
                    border: '1px solid #e0e0e0',
                    borderRadius: '8px',
                    boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)'
                  }} 
                />
                <Area 
                  type="monotone" 
                  dataKey="income" 
                  stackId="1" 
                  stroke="#10B981" 
                  fill="#10B981" 
                  fillOpacity={0.6}
                />
                <Area 
                  type="monotone" 
                  dataKey="expenses" 
                  stackId="2" 
                  stroke="#EF4444" 
                  fill="#EF4444" 
                  fillOpacity={0.6}
                />
              </AreaChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card className="glass-card animate-fade-in" style={{ animationDelay: '0.5s' }}>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <PiggyBank className="h-5 w-5 text-primary" />
              Expense Categories
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={categoryData}
                  cx="50%"
                  cy="50%"
                  outerRadius={80}
                  dataKey="value"
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                >
                  {categoryData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip 
                  formatter={(value) => [`$${value}`, 'Amount']}
                  contentStyle={{ 
                    backgroundColor: 'white', 
                    border: '1px solid #e0e0e0',
                    borderRadius: '8px'
                  }} 
                />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      {/* Recent Activity & Budget Overview */}
      <div className="grid gap-6 md:grid-cols-2">
        <Card className="glass-card animate-fade-in" style={{ animationDelay: '0.6s' }}>
          <CardHeader>
            <CardTitle>Recent Transactions</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {recentTransactions.map((transaction) => (
                <div key={transaction.id} className="flex items-center justify-between p-3 rounded-lg bg-muted/30 hover:bg-muted/50 transition-colors">
                  <div className="flex-1">
                    <p className="font-medium">{transaction.description}</p>
                    <p className="text-sm text-muted-foreground">{transaction.category} • {transaction.date}</p>
                  </div>
                  <div className={`font-bold ${transaction.amount > 0 ? 'text-success' : 'text-destructive'}`}>
                    {transaction.amount > 0 ? '+' : ''}${Math.abs(transaction.amount).toFixed(2)}
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card className="glass-card animate-fade-in" style={{ animationDelay: '0.7s' }}>
          <CardHeader>
            <CardTitle>Budget Overview</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {budgetData.map((budget, index) => (
                <div key={index} className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="font-medium">{budget.category}</span>
                    <span className="text-muted-foreground">
                      ${budget.spent} / ${budget.budget}
                    </span>
                  </div>
                  <Progress 
                    value={budget.percentage} 
                    className={`h-2 ${budget.percentage > 90 ? 'bg-red-100' : budget.percentage > 75 ? 'bg-yellow-100' : 'bg-green-100'}`}
                  />
                  <div className="text-xs text-muted-foreground">
                    {budget.percentage.toFixed(1)}% used
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Dashboard;