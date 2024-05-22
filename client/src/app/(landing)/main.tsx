import Image from "next/image";
import Logo from "./assets/logo.png";
const LandingPage = () => {
  return (
    <>
      <div className="w-full flex gap-20 justify-start py-5 px-10 bg-primary">
        <div className="w-[10rem]">
          <Image src={Logo} alt="image"  className="object-cover w-full h-full"/>
        </div>

        <div className="flex justify-center items-center gap-4 text-white">
          <div className="cursor-pointer">Home</div>
          <div className="cursor-pointer">Product</div>
          <div className="cursor-pointer">Team</div>
          <div className="cursor-pointer">About Us</div>
        </div>
      </div>
      
    </>
  );
};

export default LandingPage;
