
import { SidebarTrigger } from "@/components/ui/sidebar";

interface PageHeaderProps {
  title: string;
  description?: string;
  actions?: React.ReactNode;
}

export function PageHeader({ title, description, actions }: PageHeaderProps) {
  return (
    <div className="border-b bg-white/50 backdrop-blur-sm">
      <div className="flex h-16 items-center gap-4 px-6">
        <SidebarTrigger className="hover:bg-primary/10" />
        <div className="flex-1">
          <h1 className="text-2xl font-bold text-gradient-orange">{title}</h1>
          {description && (
            <p className="text-sm text-muted-foreground">{description}</p>
          )}
        </div>
        {actions && <div className="flex items-center gap-2">{actions}</div>}
      </div>
    </div>
  );
}
