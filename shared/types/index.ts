export interface Transaction {
  id: number;
  amount: number;
  description: string;
  category: string;
  date: string;
  type: 'income' | 'expense';
  recurring?: boolean;
  recurringFrequency?: string;
  notes?: string;
}

export interface Budget {
  id: number;
  category: string;
  amount: number;
  spent: number;
  month: string;
  notes?: string;
}

export interface WishlistItem {
  id: number;
  name: string;
  price: number;
  priority: 'high' | 'medium' | 'low';
  url?: string;
  notes?: string;
  targetDate?: string;
  saved: number;
}

export interface FinancialStats {
  totalIncome: number;
  totalExpenses: number;
  currentSavings: number;
  budgetUtilization: number;
  savingsRate: number;
}

export interface ChartData {
  month: string;
  income: number;
  expenses: number;
  savings: number;
}

export interface CategoryData {
  name: string;
  value: number;
  color: string;
}