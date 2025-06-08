
import { useState } from "react";
import { PageHeader } from "@/components/layout/PageHeader";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { Progress } from "@/components/ui/progress";
import { Plus, ExternalLink, Trash2 } from "lucide-react";
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";

interface WishlistItem {
  id: number;
  name: string;
  price: number;
  priority: string;
  url?: string;
  notes?: string;
  targetDate?: string;
  saved: number;
}

const Wishlist = () => {
  const [wishlistItems, setWishlistItems] = useState<WishlistItem[]>([
    {
      id: 1,
      name: "New Laptop",
      price: 1200.00,
      priority: "high",
      url: "https://example.com/laptop",
      notes: "For work and personal use",
      targetDate: "2023-12-15",
      saved: 400.00
    },
    {
      id: 2,
      name: "Vacation to Hawaii",
      price: 3000.00,
      priority: "medium",
      notes: "Summer vacation next year",
      targetDate: "2024-06-01",
      saved: 800.00
    },
    {
      id: 3,
      name: "New Phone",
      price: 800.00,
      priority: "low",
      url: "https://example.com/phone",
      notes: "Current one still works fine",
      saved: 200.00
    }
  ]);

  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [newItem, setNewItem] = useState({
    name: "",
    price: "",
    priority: "",
    url: "",
    notes: "",
    targetDate: "",
    saved: ""
  });

  const priorities = ["high", "medium", "low"];

  const handleAddItem = () => {
    if (newItem.name && newItem.price && newItem.priority) {
      const item: WishlistItem = {
        id: Date.now(),
        name: newItem.name,
        price: parseFloat(newItem.price),
        priority: newItem.priority,
        url: newItem.url || undefined,
        notes: newItem.notes || undefined,
        targetDate: newItem.targetDate || undefined,
        saved: parseFloat(newItem.saved) || 0
      };
      setWishlistItems([item, ...wishlistItems]);
      setNewItem({
        name: "",
        price: "",
        priority: "",
        url: "",
        notes: "",
        targetDate: "",
        saved: ""
      });
      setIsDialogOpen(false);
    }
  };

  const handleDeleteItem = (id: number) => {
    setWishlistItems(wishlistItems.filter(item => item.id !== id));
  };

  const totalWishlistValue = wishlistItems.reduce((sum, item) => sum + item.price, 0);
  const totalSaved = wishlistItems.reduce((sum, item) => sum + item.saved, 0);
  const savingsProgress = totalWishlistValue > 0 ? (totalSaved / totalWishlistValue) * 100 : 0;

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case "high": return "text-red-600 bg-red-50 border-red-200";
      case "medium": return "text-orange-600 bg-orange-50 border-orange-200";
      case "low": return "text-green-600 bg-green-50 border-green-200";
      default: return "text-gray-600 bg-gray-50 border-gray-200";
    }
  };

  return (
    <div className="flex-1 space-y-6 p-6 pt-0">
      <PageHeader
        title="Wishlist"
        description="Your savings goals and wishlist items"
        actions={
          <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
            <DialogTrigger asChild>
              <Button className="bg-primary text-primary-foreground hover:bg-primary/90">
                <Plus className="h-4 w-4 mr-2" />
                Add Wishlist Item
              </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[425px]">
              <DialogHeader>
                <DialogTitle>Add New Wishlist Item</DialogTitle>
                <DialogDescription>
                  Add something you're saving for.
                </DialogDescription>
              </DialogHeader>
              <div className="grid gap-4 py-4">
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="name" className="text-right">Name</Label>
                  <Input
                    id="name"
                    placeholder="What do you want?"
                    className="col-span-3"
                    value={newItem.name}
                    onChange={(e) => setNewItem({ ...newItem, name: e.target.value })}
                  />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="price" className="text-right">Price</Label>
                  <Input
                    id="price"
                    type="number"
                    step="0.01"
                    placeholder="0.00"
                    className="col-span-3"
                    value={newItem.price}
                    onChange={(e) => setNewItem({ ...newItem, price: e.target.value })}
                  />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="priority" className="text-right">Priority</Label>
                  <Select
                    value={newItem.priority}
                    onValueChange={(value) => setNewItem({ ...newItem, priority: value })}
                  >
                    <SelectTrigger className="col-span-3">
                      <SelectValue placeholder="Select priority" />
                    </SelectTrigger>
                    <SelectContent>
                      {priorities.map((priority) => (
                        <SelectItem key={priority} value={priority}>
                          {priority.charAt(0).toUpperCase() + priority.slice(1)}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="saved" className="text-right">Already Saved</Label>
                  <Input
                    id="saved"
                    type="number"
                    step="0.01"
                    placeholder="0.00"
                    className="col-span-3"
                    value={newItem.saved}
                    onChange={(e) => setNewItem({ ...newItem, saved: e.target.value })}
                  />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="targetDate" className="text-right">Target Date</Label>
                  <Input
                    id="targetDate"
                    type="date"
                    className="col-span-3"
                    value={newItem.targetDate}
                    onChange={(e) => setNewItem({ ...newItem, targetDate: e.target.value })}
                  />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="url" className="text-right">URL</Label>
                  <Input
                    id="url"
                    placeholder="https://..."
                    className="col-span-3"
                    value={newItem.url}
                    onChange={(e) => setNewItem({ ...newItem, url: e.target.value })}
                  />
                </div>
                <div className="grid grid-cols-4 items-center gap-4">
                  <Label htmlFor="notes" className="text-right">Notes</Label>
                  <Textarea
                    id="notes"
                    placeholder="Additional notes..."
                    className="col-span-3"
                    value={newItem.notes}
                    onChange={(e) => setNewItem({ ...newItem, notes: e.target.value })}
                  />
                </div>
              </div>
              <div className="flex justify-end gap-2">
                <Button variant="outline" onClick={() => setIsDialogOpen(false)}>
                  Cancel
                </Button>
                <Button onClick={handleAddItem}>Add Item</Button>
              </div>
            </DialogContent>
          </Dialog>
        }
      />

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Wishlist Value</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-gradient-orange">${totalWishlistValue.toFixed(2)}</div>
            <p className="text-xs text-muted-foreground">{wishlistItems.length} items</p>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Saved</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">${totalSaved.toFixed(2)}</div>
            <p className="text-xs text-muted-foreground">{savingsProgress.toFixed(1)}% of goal</p>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-6">
        {wishlistItems.map((item) => {
          const progress = item.price > 0 ? (item.saved / item.price) * 100 : 0;
          const remaining = item.price - item.saved;
          
          return (
            <Card key={item.id}>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle className="text-lg">{item.name}</CardTitle>
                    <div className="flex items-center gap-2 mt-1">
                      <span className={`text-xs px-2 py-1 rounded-full border ${getPriorityColor(item.priority)}`}>
                        {item.priority.charAt(0).toUpperCase() + item.priority.slice(1)} Priority
                      </span>
                      {item.targetDate && (
                        <span className="text-xs text-muted-foreground">
                          Target: {new Date(item.targetDate).toLocaleDateString()}
                        </span>
                      )}
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <span className="text-lg font-bold text-gradient-orange">
                      ${item.price.toFixed(2)}
                    </span>
                    {item.url && (
                      <Button variant="ghost" size="sm" asChild>
                        <a href={item.url} target="_blank" rel="noopener noreferrer">
                          <ExternalLink className="h-4 w-4" />
                        </a>
                      </Button>
                    )}
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleDeleteItem(item.id)}
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              </CardHeader>
              <CardContent>
                <div className="space-y-2">
                  <Progress value={progress} className="w-full" />
                  <div className="flex justify-between text-sm">
                    <span className="text-green-600">
                      ${item.saved.toFixed(2)} saved
                    </span>
                    <span className="text-muted-foreground">
                      ${remaining.toFixed(2)} remaining
                    </span>
                  </div>
                  {item.notes && (
                    <p className="text-xs text-muted-foreground mt-2">{item.notes}</p>
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

export default Wishlist;
