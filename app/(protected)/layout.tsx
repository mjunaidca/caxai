import SideNav from '@/components/dashboard/sidenav';

export default function Layout({ children }: { children: React.ReactNode }) {

  return (
    <div className="flex h-screen flex-col md:flex-row md:overflow-hidden">
      <div className="w-full flex-none md:max-w-96">
        <SideNav />
      </div>
      <div className="grow p-7 md:overflow-y-auto md:p-10 xl:p-12">{children}</div>
    </div>
  );
}
