import { LogoutButton } from "@/components/auth/logout-button";
import { Button } from "@/components/ui/button";

const page = () => {
  return (
    <div>
      <LogoutButton>
        <Button>Logout</Button> 

        </LogoutButton>
    </div>
  );
};

export default page;
