
import {
  DollarSign,
  TrendingUp,
  TrendingDown,
  PiggyBank,
  Heart,
  BarChart3,
  Home,
  Wallet,
  User
} from "lucide-react";
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar";
import { useLocation, Link } from "react-router-dom";
import { useAuth } from "@/contexts/AuthContext";

const menuItems = [
  {
    title: "Dashboard",
    url: "/",
    icon: Home,
  },
  {
    title: "Expenses",
    url: "/expenses",
    icon: TrendingDown,
  },
  {
    title: "Income",
    url: "/income",
    icon: TrendingUp,
  },
  {
    title: "Budget",
    url: "/budget",
    icon: PiggyBank,
  },
  {
    title: "Wishlist",
    url: "/wishlist",
    icon: Heart,
  },
  {
    title: "Reports",
    url: "/reports",
    icon: BarChart3,
  },
  {
    title: "Profile",
    url: "/profile",
    icon: User,
  },
];

export function AppSidebar() {
  const location = useLocation();
  const { user } = useAuth();

  return (
    <Sidebar className="border-r-0">
      <SidebarHeader className="border-b border-sidebar-border p-4">
        <div className="flex items-center gap-3">
          <div className="gradient-orange p-2 rounded-lg">
            <Wallet className="h-6 w-6 text-white" />
          </div>
          <div>
            <h1 className="text-xl font-bold text-gradient-orange">FinFlow</h1>
            <p className="text-sm text-muted-foreground">Financial Manager</p>
          </div>
        </div>
      </SidebarHeader>
      
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel className="text-xs uppercase tracking-wider text-muted-foreground px-3 py-2">
            Navigation
          </SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {menuItems.map((item) => {
                const isActive = location.pathname === item.url;
                return (
                  <SidebarMenuItem key={item.title}>
                    <SidebarMenuButton
                      asChild
                      className={`group transition-all duration-200 ${
                        isActive 
                          ? "bg-primary text-primary-foreground hover:bg-primary/90" 
                          : "hover:bg-sidebar-accent hover:text-sidebar-accent-foreground"
                      }`}
                    >
                      <Link to={item.url} className="flex items-center gap-3 px-3 py-2">
                        <item.icon className={`h-5 w-5 transition-transform group-hover:scale-110 ${
                          isActive ? "text-white" : ""
                        }`} />
                        <span className="font-medium">{item.title}</span>
                      </Link>
                    </SidebarMenuButton>
                  </SidebarMenuItem>
                );
              })}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
      
      <SidebarFooter className="border-t border-sidebar-border p-4">
        <div className="flex items-center gap-3 px-3 py-2">
          <div className="h-8 w-8 rounded-full gradient-orange flex items-center justify-center">
            <User className="h-4 w-4 text-white" />
          </div>
          <div className="flex-1">
            <p className="text-sm font-medium">
              {user?.first_name && user?.last_name 
                ? `${user.first_name} ${user.last_name}`
                : user?.username || 'User'
              }
            </p>
            <p className="text-xs text-muted-foreground">{user?.email}</p>
          </div>
        </div>
      </SidebarFooter>
    </Sidebar>
  );
}
