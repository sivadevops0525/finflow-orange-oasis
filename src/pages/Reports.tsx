
import { PageHeader } from "@/components/layout/PageHeader";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, LineChart, Line } from "recharts";

const Reports = () => {
  // Sample data for charts
  const monthlyData = [
    { month: 'Jan', income: 3500, expenses: 2800, savings: 700 },
    { month: 'Feb', income: 3500, expenses: 3200, savings: 300 },
    { month: 'Mar', income: 4000, expenses: 2900, savings: 1100 },
    { month: 'Apr', income: 3500, expenses: 3100, savings: 400 },
    { month: 'May', income: 3500, expenses: 2700, savings: 800 },
    { month: 'Jun', income: 3800, expenses: 3000, savings: 800 },
  ];

  const categoryData = [
    { name: 'Housing', value: 1200, color: '#FF6B35' },
    { name: 'Food & Dining', value: 450, color: '#F7931E' },
    { name: 'Transportation', value: 200, color: '#FFD23F' },
    { name: 'Entertainment', value: 150, color: '#06D6A0' },
    { name: 'Bills & Utilities', value: 300, color: '#118AB2' },
    { name: 'Shopping', value: 250, color: '#073B4C' },
  ];

  const savingsData = [
    { month: 'Jan', amount: 700 },
    { month: 'Feb', amount: 1000 },
    { month: 'Mar', amount: 2100 },
    { month: 'Apr', amount: 2500 },
    { month: 'May', amount: 3300 },
    { month: 'Jun', amount: 4100 },
  ];

  const totalIncome = monthlyData.reduce((sum, month) => sum + month.income, 0);
  const totalExpenses = monthlyData.reduce((sum, month) => sum + month.expenses, 0);
  const totalSavings = totalIncome - totalExpenses;
  const savingsRate = totalIncome > 0 ? (totalSavings / totalIncome) * 100 : 0;

  return (
    <div className="flex-1 space-y-6 p-6 pt-0">
      <PageHeader
        title="Reports"
        description="Detailed financial reports and analytics"
        actions={
          <Select defaultValue="6months">
            <SelectTrigger className="w-[180px]">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="1month">Last Month</SelectItem>
              <SelectItem value="3months">Last 3 Months</SelectItem>
              <SelectItem value="6months">Last 6 Months</SelectItem>
              <SelectItem value="1year">Last Year</SelectItem>
            </SelectContent>
          </Select>
        }
      />

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Income</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">${totalIncome.toFixed(2)}</div>
            <p className="text-xs text-muted-foreground">Last 6 months</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Expenses</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-red-600">${totalExpenses.toFixed(2)}</div>
            <p className="text-xs text-muted-foreground">Last 6 months</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Net Savings</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-gradient-orange">${totalSavings.toFixed(2)}</div>
            <p className="text-xs text-muted-foreground">Last 6 months</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Savings Rate</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-gradient-orange">{savingsRate.toFixed(1)}%</div>
            <p className="text-xs text-muted-foreground">Of total income</p>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Monthly Income vs Expenses</CardTitle>
            <CardDescription>Track your financial performance over time</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={monthlyData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="month" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="income" fill="#06D6A0" name="Income" />
                <Bar dataKey="expenses" fill="#FF6B35" name="Expenses" />
              </BarChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Expense Categories</CardTitle>
            <CardDescription>Breakdown of your spending by category</CardDescription>
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
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Savings Trend</CardTitle>
          <CardDescription>Your cumulative savings over time</CardDescription>
        </CardHeader>
        <CardContent>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={savingsData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="month" />
              <YAxis />
              <Tooltip />
              <Line 
                type="monotone" 
                dataKey="amount" 
                stroke="#FF6B35" 
                strokeWidth={3}
                dot={{ fill: '#FF6B35', strokeWidth: 2, r: 6 }}
                name="Cumulative Savings"
              />
            </LineChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>

      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Top Expense Categories</CardTitle>
            <CardDescription>Your highest spending categories this period</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {categoryData
                .sort((a, b) => b.value - a.value)
                .slice(0, 5)
                .map((category, index) => (
                  <div key={category.name} className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <div 
                        className="w-3 h-3 rounded-full" 
                        style={{ backgroundColor: category.color }}
                      />
                      <span className="font-medium">{category.name}</span>
                    </div>
                    <span className="text-gradient-orange font-semibold">
                      ${category.value.toFixed(2)}
                    </span>
                  </div>
                ))}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Financial Health Score</CardTitle>
            <CardDescription>Based on your spending and saving patterns</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <span>Savings Rate</span>
                <span className="font-semibold text-green-600">Good ({savingsRate.toFixed(1)}%)</span>
              </div>
              <div className="flex items-center justify-between">
                <span>Budget Adherence</span>
                <span className="font-semibold text-green-600">Excellent (95%)</span>
              </div>
              <div className="flex items-center justify-between">
                <span>Debt-to-Income</span>
                <span className="font-semibold text-green-600">Low (12%)</span>
              </div>
              <div className="flex items-center justify-between">
                <span>Emergency Fund</span>
                <span className="font-semibold text-orange-600">Moderate (3 months)</span>
              </div>
              <div className="pt-4 border-t">
                <div className="text-center">
                  <div className="text-3xl font-bold text-gradient-orange">85</div>
                  <div className="text-sm text-muted-foreground">Overall Score</div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Reports;
