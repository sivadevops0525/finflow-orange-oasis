
import { PageHeader } from "@/components/layout/PageHeader";

const Expenses = () => {
  return (
    <div className="flex-1 space-y-6 p-6 pt-0">
      <PageHeader
        title="Expenses"
        description="Track and manage your expenses"
      />
      <div className="flex items-center justify-center h-64">
        <p className="text-muted-foreground">Expenses page coming soon...</p>
      </div>
    </div>
  );
};

export default Expenses;
