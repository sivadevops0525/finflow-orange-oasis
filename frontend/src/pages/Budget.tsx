
import { useState } from "react";
import { PageHeader } from "@/components/layout/PageHeader";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Progress } from "@/components/ui/progress";
import { Plus, Edit, Trash2 } from "lucide-react";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";

interface Budget {
  id: number;
  category: string;
  amount: number;
  spent: number;
  month: string;
  notes?: string;
}

const Budget = () => {
  const [budgets, setBudgets] = useState<Budget[]>([
    {
      id: 1,
      category: "Food & Dining",
      amount: 500.00,
      spent: 120.50,
      month: "2023-09",
      notes: "Monthly food budget"
    },
    {
      id: 2,
      category: "Housing",
      amount: 1500.00,
      spent: 1200.00,
      month: "2023-09",
      notes: "Rent and utilities"
    },
    {
      id: 3,
      category: "Transportation",
      amount: 200.00,
      spent: 50.25,
      month: "2023-09",
      notes: "Gas and public transit"
    },
    {
      id: 4,
      category: "Entertainment",
      amount: 100.00,
      spent: 9.99,
      month: "2023-09",
      notes: "Subscriptions and activities"
    }
  ]);

  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [newBudget, setNewBudget] = useState({
    category: "",
    amount: "",
    month: "",
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

  const handleAddBudget = () => {
    if (newBudget.category && newBudget.amount && newBudget.month) {
      const budget: Budget = {
        id: Date.now(),
        category: newBudget.category,
        amount: parseFloat(newBudget.amount),
        spent: 0,
        month: newBudget.month,
        notes: newBudget.notes
      };
      setBudgets([budget, ...budgets]);
      setNewBudget({
        category: "",
        amount: "",
        month: "",
        notes: ""
      });
      setIsDialogOpen(false);
    }
  };

  const handleDeleteBudget = (id: number) => {
    setBudgets(budgets.filter(budget => budget.id !== id));
  };

  const totalBudget = budgets.reduce((sum, budget) => sum + budget.amount, 0);
  const totalSpent = budgets.reduce((sum, budget) => sum + budget.spent, 0);
  const totalRemaining = totalBudget - totalSpent;

  return (
    <div className="flex-1 space-y-6 p-6 pt-0">
      <PageHeader
        title="Budget"
        description="Plan and monitor your budget"
        actions={
          <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
            <DialogTrigger asChild>
              <Button className="bg-primary text-primary-foreground hover:bg-primary/90">
                <Plus className="h-4 w-4 mr-2" />
                Add Budget
              </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[425px]">
              <DialogHeader>
                <DialogTitle>Add New Budget</DialogTitle>
                <DialogDescription>
                  Set a budget for a category and month.
                </DialogDescription>
              </DialogHeader>
              <div className="grid gap-4 py-4">
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="category" className="text-right">Category</Label>
                  <Select
                    value={newBudget.category}
                    onValueChange={(value) => setNewBudget({ ...newBudget, category: value })}
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
                  <Label htmlFor="amount" className="text-right">Amount</Label>
                  <Input
                    id="amount"
                    type="number"
                    step="0.01"
                    placeholder="0.00"
                    className="col-span-3"
                    value={newBudget.amount}
                    onChange={(e) => setNewBudget({ ...newBudget, amount: e.target.value })}
                  />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="month" className="text-right">Month</Label>
                  <Input
                    id="month"
                    type="month"
                    className="col-span-3"
                    value={newBudget.month}
                    onChange={(e) => setNewBudget({ ...newBudget, month: e.target.value })}
                  />
                </div>
              </div>
              <div className="flex justify-end gap-2">
                <Button variant="outline" onClick={() => setIsDialogOpen(false)}>
                  Cancel
                </Button>
                <Button onClick={handleAddBudget}>Add Budget</Button>
              </div>
            </DialogContent>
          </Dialog>
        }
      />

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Budget</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-gradient-orange">${totalBudget.toFixed(2)}</div>
            <p className="text-xs text-muted-foreground">This month</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Spent</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-red-600">${totalSpent.toFixed(2)}</div>
            <p className="text-xs text-muted-foreground">This month</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Remaining</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">${totalRemaining.toFixed(2)}</div>
            <p className="text-xs text-muted-foreground">Available</p>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-6">
        {budgets.map((budget) => {
          const percentage = (budget.spent / budget.amount) * 100;
          const remaining = budget.amount - budget.spent;
          
          return (
            <Card key={budget.id}>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle className="text-lg">{budget.category}</CardTitle>
                    <CardDescription>{budget.month}</CardDescription>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-sm text-muted-foreground">
                      ${budget.spent.toFixed(2)} / ${budget.amount.toFixed(2)}
                    </span>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleDeleteBudget(budget.id)}
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <Progress value={percentage} className="w-full" />
                  <div className="flex justify-between text-sm">
                    <span className={remaining >= 0 ? "text-green-600" : "text-red-600"}>
                      ${remaining.toFixed(2)} remaining
                    </span>
                    <span className="text-muted-foreground">
                      {percentage.toFixed(1)}% used
                    </span>
                  </div>
                  {budget.notes && (
                    <p className="text-xs text-muted-foreground mt-2">{budget.notes}</p>
                  )}
                </div>
              </CardContent>
            </Card>
          );
        })}
      </div>
    </div>
  );
};

export default Budget;
