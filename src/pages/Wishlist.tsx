
import { PageHeader } from "@/components/layout/PageHeader";

const Wishlist = () => {
  return (
    <div className="flex-1 space-y-6 p-6 pt-0">
      <PageHeader
        title="Wishlist"
        description="Your savings goals and wishlist items"
      />
      <div className="flex items-center justify-center h-64">
        <p className="text-muted-foreground">Wishlist page coming soon...</p>
      </div>
    </div>
  );
};

export default Wishlist;
