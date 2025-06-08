
import { useState } from "react";
import { PageHeader } from "@/components/layout/PageHeader";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { Plus, Edit, Trash2 } from "lucide-react";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";

interface Expense {
  id: number;
  amount: number;
  description: string;
  category: string;
  date: string;
  recurring: boolean;
  recurringFrequency?: string;
  notes?: string;
}

const Expenses = () => {
  const [expenses, setExpenses] = useState<Expense[]>([
    {
      id: 1,
      amount: 120.50,
      description: "Grocery shopping",
      category: "Food & Dining",
      date: "2023-09-05",
      recurring: false,
      notes: ""
    },
    {
      id: 2,
      amount: 50.25,
      description: "Gas station",
      category: "Transportation",
      date: "2023-09-07",
      recurring: false,
      notes: ""
    },
    {
      id: 3,
      amount: 9.99,
      description: "Netflix subscription",
      category: "Entertainment",
      date: "2023-09-01",
      recurring: true,
      recurringFrequency: "Monthly",
      notes: "Streaming service"
    }
  ]);

  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [newExpense, setNewExpense] = useState({
    amount: "",
    description: "",
    category: "",
    date: "",
    recurring: false,
    recurringFrequency: "",
    notes: ""
  });

  const categories = [
    "Food & Dining",
    "Transportation",
    "Entertainment",
    "Housing",
    "Bills & Utilities",
    "Shopping",
    "Healthcare",
    "Other"
  ];

  const handleAddExpense = () => {
    if (newExpense.amount && newExpense.description && newExpense.category && newExpense.date) {
      const expense: Expense = {
        id: Date.now(),
        amount: parseFloat(newExpense.amount),
        description: newExpense.description,
        category: newExpense.category,
        date: newExpense.date,
        recurring: newExpense.recurring,
        recurringFrequency: newExpense.recurring ? newExpense.recurringFrequency : undefined,
        notes: newExpense.notes
      };
      setExpenses([expense, ...expenses]);
      setNewExpense({
        amount: "",
        description: "",
        category: "",
        date: "",
        recurring: false,
        recurringFrequency: "",
        notes: ""
      });
      setIsDialogOpen(false);
    }
  };

  const handleDeleteExpense = (id: number) => {
    setExpenses(expenses.filter(expense => expense.id !== id));
  };

  const totalExpenses = expenses.reduce((sum, expense) => sum + expense.amount, 0);

  return (
    <div className="flex-1 space-y-6 p-6 pt-0">
      <PageHeader
        title="Expenses"
        description="Track and manage your expenses"
        actions={
          <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
            <DialogTrigger asChild>
              <Button className="bg-primary text-primary-foreground hover:bg-primary/90">
                <Plus className="h-4 w-4 mr-2" />
                Add Expense
              </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[425px]">
              <DialogHeader>
                <DialogTitle>Add New Expense</DialogTitle>
                <DialogDescription>
                  Enter the details of your expense below.
                </DialogDescription>
              </DialogHeader>
              <div className="grid gap-4 py-4">
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="amount" className="text-right">Amount</Label>
                  <Input
                    id="amount"
                    type="number"
                    step="0.01"
                    placeholder="0.00"
                    className="col-span-3"
                    value={newExpense.amount}
                    onChange={(e) => setNewExpense({ ...newExpense, amount: e.target.value })}
                  />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="description" className="text-right">Description</Label>
                  <Input
                    id="description"
                    placeholder="What did you spend on?"
                    className="col-span-3"
                    value={newExpense.description}
                    onChange={(e) => setNewExpense({ ...newExpense, description: e.target.value })}
                  />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="category" className="text-right">Category</Label>
                  <Select
                    value={newExpense.category}
                    onValueChange={(value) => setNewExpense({ ...newExpense, category: value })}
                  >
                    <SelectTrigger className="col-span-3">
                      <SelectValue placeholder="Select category" />
                    </SelectTrigger>
                    <SelectContent>
                      {categories.map((category) => (
                        <SelectItem key={category} value={category}>
                          {category}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="date" className="text-right">Date</Label>
                  <Input
                    id="date"
                    type="date"
                    className="col-span-3"
                    value={newExpense.date}
                    onChange={(e) => setNewExpense({ ...newExpense, date: e.target.value })}
                  />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="notes" className="text-right">Notes</Label>
                  <Textarea
                    id="notes"
                    placeholder="Additional notes..."
                    className="col-span-3"
                    value={newExpense.notes}
                    onChange={(e) => setNewExpense({ ...newExpense, notes: e.target.value })}
                  />
                </div>
              </div>
              <div className="flex justify-end gap-2">
                <Button variant="outline" onClick={() => setIsDialogOpen(false)}>
                  Cancel
                </Button>
                <Button onClick={handleAddExpense}>Add Expense</Button>
              </div>
            </DialogContent>
          </Dialog>
        }
      />

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Expenses</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-gradient-orange">${totalExpenses.toFixed(2)}</div>
            <p className="text-xs text-muted-foreground">This month</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Categories</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{new Set(expenses.map(e => e.category)).size}</div>
            <p className="text-xs text-muted-foreground">Active categories</p>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Recent Expenses</CardTitle>
          <CardDescription>Your latest expense transactions</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {expenses.map((expense) => (
              <div key={expense.id} className="flex items-center justify-between p-4 border rounded-lg">
                <div className="flex-1">
                  <div className="flex items-center gap-4">
                    <div>
                      <p className="font-medium">{expense.description}</p>
                      <p className="text-sm text-muted-foreground">{expense.category} • {expense.date}</p>
                      {expense.notes && (
                        <p className="text-xs text-muted-foreground mt-1">{expense.notes}</p>
                      )}
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-lg font-semibold text-gradient-orange">
                    ${expense.amount.toFixed(2)}
                  </span>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => handleDeleteExpense(expense.id)}
                  >
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default Expenses;
