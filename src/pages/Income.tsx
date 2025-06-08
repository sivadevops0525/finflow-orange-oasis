
import { useState } from "react";
import { PageHeader } from "@/components/layout/PageHeader";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Plus, Trash2 } from "lucide-react";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";

interface Income {
  id: number;
  amount: number;
  source: string;
  date: string;
  recurring: boolean;
  recurringFrequency?: string;
  notes?: string;
}

const Income = () => {
  const [incomes, setIncomes] = useState<Income[]>([
    {
      id: 1,
      amount: 3500.00,
      source: "Salary",
      date: "2023-09-01",
      recurring: true,
      recurringFrequency: "Monthly",
      notes: "Monthly salary"
    },
    {
      id: 2,
      amount: 500.00,
      source: "Freelance work",
      date: "2023-09-15",
      recurring: false,
      notes: "Website design project"
    },
    {
      id: 3,
      amount: 50.00,
      source: "Interest",
      date: "2023-09-30",
      recurring: true,
      recurringFrequency: "Monthly",
      notes: "Savings account interest"
    }
  ]);

  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [newIncome, setNewIncome] = useState({
    amount: "",
    source: "",
    date: "",
    recurring: false,
    recurringFrequency: "",
    notes: ""
  });

  const handleAddIncome = () => {
    if (newIncome.amount && newIncome.source && newIncome.date) {
      const income: Income = {
        id: Date.now(),
        amount: parseFloat(newIncome.amount),
        source: newIncome.source,
        date: newIncome.date,
        recurring: newIncome.recurring,
        recurringFrequency: newIncome.recurring ? newIncome.recurringFrequency : undefined,
        notes: newIncome.notes
      };
      setIncomes([income, ...incomes]);
      setNewIncome({
        amount: "",
        source: "",
        date: "",
        recurring: false,
        recurringFrequency: "",
        notes: ""
      });
      setIsDialogOpen(false);
    }
  };

  const handleDeleteIncome = (id: number) => {
    setIncomes(incomes.filter(income => income.id !== id));
  };

  const totalIncome = incomes.reduce((sum, income) => sum + income.amount, 0);
  const monthlyRecurring = incomes.filter(income => income.recurring).reduce((sum, income) => sum + income.amount, 0);

  return (
    <div className="flex-1 space-y-6 p-6 pt-0">
      <PageHeader
        title="Income"
        description="Track your income sources"
        actions={
          <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
            <DialogTrigger asChild>
              <Button className="bg-primary text-primary-foreground hover:bg-primary/90">
                <Plus className="h-4 w-4 mr-2" />
                Add Income
              </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[425px]">
              <DialogHeader>
                <DialogTitle>Add New Income</DialogTitle>
                <DialogDescription>
                  Enter the details of your income source below.
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
                    value={newIncome.amount}
                    onChange={(e) => setNewIncome({ ...newIncome, amount: e.target.value })}
                  />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="source" className="text-right">Source</Label>
                  <Input
                    id="source"
                    placeholder="Income source"
                    className="col-span-3"
                    value={newIncome.source}
                    onChange={(e) => setNewIncome({ ...newIncome, source: e.target.value })}
                  />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="date" className="text-right">Date</Label>
                  <Input
                    id="date"
                    type="date"
                    className="col-span-3"
                    value={newIncome.date}
                    onChange={(e) => setNewIncome({ ...newIncome, date: e.target.value })}
                  />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="notes" className="text-right">Notes</Label>
                  <Textarea
                    id="notes"
                    placeholder="Additional notes..."
                    className="col-span-3"
                    value={newIncome.notes}
                    onChange={(e) => setNewIncome({ ...newIncome, notes: e.target.value })}
                  />
                </div>
              </div>
              <div className="flex justify-end gap-2">
                <Button variant="outline" onClick={() => setIsDialogOpen(false)}>
                  Cancel
                </Button>
                <Button onClick={handleAddIncome}>Add Income</Button>
              </div>
            </DialogContent>
          </Dialog>
        }
      />

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Income</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-gradient-orange">${totalIncome.toFixed(2)}</div>
            <p className="text-xs text-muted-foreground">This month</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Monthly Recurring</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">${monthlyRecurring.toFixed(2)}</div>
            <p className="text-xs text-muted-foreground">Recurring income</p>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Income Sources</CardTitle>
          <CardDescription>Your income transactions</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {incomes.map((income) => (
              <div key={income.id} className="flex items-center justify-between p-4 border rounded-lg">
                <div className="flex-1">
                  <div className="flex items-center gap-4">
                    <div>
                      <p className="font-medium">{income.source}</p>
                      <p className="text-sm text-muted-foreground">
                        {income.date}
                        {income.recurring && ` • Recurring ${income.recurringFrequency}`}
                      </p>
                      {income.notes && (
                        <p className="text-xs text-muted-foreground mt-1">{income.notes}</p>
                      )}
                    </div>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-lg font-semibold text-green-600">
                    +${income.amount.toFixed(2)}
                  </span>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => handleDeleteIncome(income.id)}
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

export default Income;
