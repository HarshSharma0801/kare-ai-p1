"use client";
import { useState } from "react";
import axios from "axios";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";
import { FaLink } from "react-icons/fa6";
import { RotatingLines } from "react-loader-spinner";
import React from "react";
import BarChart from "../components/BarChart";

const MainForm = () => {
  const [selectedIndustry, setSelectedIndustry] = useState<number | null>(null);
  const [industry, setIndustry] = useState<string | null>(null);
  const [subIndustry, setSubIndustry] = useState<string | null>(null);
  const [region, setRegion] = useState<string | null>(null);
  const [compValue, setCompValue] = useState<string>("");

  const [loading, setLoading] = useState(false);
  const [sections, setSections] = useState({
    industryTrends: { visible: false, loading: false },
    topCompetitors: { visible: false, loading: false },
    technologicalTrends: { visible: false, loading: false },
    top5Predictions: { visible: false, loading: false },
    industryNews: { visible: false, loading: false },
    keyTakeaways: { visible: false, loading: false },
    marketSize: { visible: false, loading: false },
  });

  const industries = [
    "Renewable Energy",
    "Healthcare Technology",
    "Artificial Intelligence",
    "Fintech (Financial Technology)",
    "Clothing Sector",
    "Smart Cities",
  ];

  const subIndustries = [
    [
      "Solar Power",
      "Wind Energy",
      "Hydrogen Energy",
      "Geothermal Energy",
      "Bioenergy",
    ],
    [
      "Telemedicine",
      "Digital Health",
      "Biotech Innovations",
      "Medical Devices",
      "Health AI",
    ],
    [
      "Machine Learning",
      "Robotics",
      "AI Ethics and Governance",
      "AI in Finance",
      "AI in Customer Service",
    ],
    [
      "Digital Banking",
      "Blockchain and Cryptocurrency",
      "Insurtech",
      "Payment Processing",
      "Regtech",
    ],
    [
      "Fast Fashion",
      "Luxury Fashion",
      "Athleisure",
      "Sustainable and Ethical Fashion",
      "Custom and Personalized Fashion",
    ],
    [
      "Smart Infrastructure",
      "Urban Mobility",
      "Public Safety",
      "Environmental Monitoring",
      "E-Governance",
    ],
  ];

  const scrollToBottom = () => {
    const targetPosition = document.body.scrollHeight;
    const startPosition = window.pageYOffset;
    const distance = targetPosition - startPosition;
    const duration = 500; // Duration of the animation in milliseconds
    let start = null;

    const step = (timestamp) => {
      if (!start) start = timestamp;
      const progress = timestamp - start;
      const currentPosition = startPosition + (distance * progress) / duration;
      window.scrollTo(0, currentPosition);
      if (progress < duration) {
        window.requestAnimationFrame(step);
      } else {
        window.scrollTo(0, targetPosition);
      }
    };

    window.requestAnimationFrame(step);
  };

  const handleIndustryChange = (e: any) => {
    const selected = e;
    setIndustry(selected);
    const index = industries.findIndex((ind) => ind === selected);
    setSelectedIndustry(index);
    setSubIndustry(null); // Reset sub-industry when industry changes
  };

  const handleSubIndustryChange = (e: any) => {
    setSubIndustry(e);
  };

  const handleRegionChange = (e: any) => {
    setRegion(e);
  };

  const handleCompValueChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setCompValue(e.target.value);
  };

  const [industryTrends, setIndustryTrends] = useState<any[]>([]);
  const [topCompetitors, setTopCompetitors] = useState<any[]>([]);
  const [technologicalTrends, setTechnologicalTrends] = useState<any[]>([]);
  const [top5Predictions, setTop5Predictions] = useState<any[]>([]);
  const [industryNews, setIndustryNews] = useState<any[]>([]);
  const [keyTakeaways, setKeyTakeaways] = useState<any[]>([]);
  const [marketSize, setMarketSize] = useState<any[]>([]);

  const fetchData = async (
    endpoint: string,
    data: object,
    setter: React.Dispatch<React.SetStateAction<any[]>>,
    section: string
  ) => {
    try {
      setSections((prev) => ({
        ...prev,
        [section]: { ...prev[section], loading: true },
      }));
      const response = await axios.post(
        `http://127.0.0.1:8000/${endpoint}`,
        data,
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      setter(response.data[endpoint]);
      setSections((prev) => ({
        ...prev,
        [section]: { visible: true, loading: false },
      }));
    } catch (error) {
      console.error(`Error fetching ${endpoint}:`, error);
      setSections((prev) => ({
        ...prev,
        [section]: { ...prev[section], loading: false },
      }));
    }
  };

  const getResult = async () => {
    setLoading(true);
    const data = {
      industry_sector: industry,
      industry_subsector: subIndustry,
      region,
      company_value_proposition: compValue,
    };

    await fetchData(
      "industry_trends",
      data,
      setIndustryTrends,
      "industryTrends"
    );
    scrollToBottom();
    await fetchData(
      "top_competitors",
      data,
      setTopCompetitors,
      "topCompetitors"
    );
    scrollToBottom();
    await fetchData(
      "technological_trends",
      data,
      setTechnologicalTrends,
      "technologicalTrends"
    );
    scrollToBottom();
    await fetchData(
      "top_5_predictions",
      data,
      setTop5Predictions,
      "top5Predictions"
    );
    scrollToBottom();
    await fetchData("market_size", data, setMarketSize, "marketSize");
    scrollToBottom();
    await fetchData("industry_news", data, setIndustryNews, "industryNews");
    scrollToBottom();
    await fetchData("key_takeaways", data, setKeyTakeaways, "keyTakeaways");
    scrollToBottom();

    setLoading(false);
  };

  return (
    <div className="w-full h-full flex flex-col md:py-40 md:px-40 py-20 px-20 justify-center">
      <div className="flex justify-center items-center flex-col gap-10">
        <div>Please Provide details below to generate Report</div>

        <div>
          <Select onValueChange={handleIndustryChange}>
            <SelectTrigger className="w-[280px] focus:ring-offset-0 focus:ring-0">
              <SelectValue placeholder="Select the Industry Sector" />
            </SelectTrigger>
            <SelectContent>
              {industries.map((data, index) => (
                <SelectItem key={index} value={data}>
                  {data}
                </SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <div>
          <Select
            onValueChange={handleSubIndustryChange}
            disabled={selectedIndustry == null}
          >
            <SelectTrigger className="w-[280px] outline-none focus:ring-offset-0 focus:ring-0">
              <SelectValue placeholder="Select the Industry Sub Sector" />
            </SelectTrigger>
            <SelectContent>
              {selectedIndustry !== null &&
                subIndustries[selectedIndustry].map((data, index) => (
                  <SelectItem key={index} value={data}>
                    {data}
                  </SelectItem>
                ))}
            </SelectContent>
          </Select>
        </div>

        <div>
          <Select onValueChange={handleRegionChange}>
            <SelectTrigger className="w-[280px] focus:ring-offset-0 focus:ring-0">
              <SelectValue placeholder="Select Region" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="india">India</SelectItem>
              <SelectItem value="worldwide">WorldWide</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <div>
          <Input
            onChange={handleCompValueChange}
            className="w-[280px] outline-none focus:ring-offset-0 focus:ring-0 focus-visible:ring-0"
            placeholder="Your Company Value Proposition"
          />
        </div>

        <div>
          <Button
            onClick={getResult}
            className="w-[280px] bg-primary text-white font-semibold"
            disabled={loading}
          >
            {loading ? "Loading..." : "Run Market Research Agent"}
          </Button>
        </div>
      </div>

      {Object.keys(sections).map((sectionKey, idx) => (
        <motion.div
          key={idx}
          initial={false}
          animate={{
            height: sections[sectionKey].visible ? "auto" : 0,
            overflow: "hidden",
          }}
        >
          <div className="flex flex-col p-16 gap-5">
            <h1 className="text-xl font-bold text-gray-700 border-b pb-2">
              {sectionKey
                .replace(/([A-Z])/g, " $1")
                .toLocaleUpperCase()
                .trim()}
            </h1>
            {sections[sectionKey].loading && <div>Loading...</div>}
            {!sections[sectionKey].loading &&
              (() => {
                switch (sectionKey) {
                  case "industryTrends":
                    return industryTrends.map((data, index) => (
                      <li key={index} className="mb-2 list-disc pl-5">
                        <span className="text-md text-gray-800">
                          {data.point}
                        </span>
                      </li>
                    ));
                  case "topCompetitors":
                    return topCompetitors.map((data, index) => (
                      <li key={index} className="mb-2 list-disc pl-5">
                        <span className="text-md text-gray-800">
                          {data.company}
                        </span>
                      </li>
                    ));
                  case "technologicalTrends":
                    return technologicalTrends.map((data, index) => (
                      <li key={index} className="mb-2 list-disc pl-5">
                        <span className="text-md text-gray-800">
                          {data.point}
                        </span>
                      </li>
                    ));
                  case "top5Predictions":
                    return top5Predictions.map((data, index) => (
                      <li key={index} className="mb-2 list-disc pl-5">
                        <span className="text-md text-gray-800">
                          {data.prediction}
                        </span>
                        <span className="flex items-center gap-[10px] text-blue-700">
                          <FaLink />
                          <a
                            className="underline"
                            href={data.source}
                            target="_blank"
                            rel="noopener noreferrer"
                          >
                            Source
                          </a>
                        </span>
                      </li>
                    ));
                  case "marketSize":
                    return <BarChart data={marketSize} />;
                  case "industryNews":
                    return (
                      <ul className="list-disc pl-5">
                        {industryNews.map((data, index) => (
                          <li key={index} className="mb-2">
                            <div className="text-md text-gray-800">
                              {data.title}
                            </div>
                            <div className="flex items-center gap-[10px] text-blue-700">
                              <FaLink />
                              <a
                                className="underline"
                                href={data.url}
                                target="_blank"
                                rel="noopener noreferrer"
                              >
                                Source
                              </a>
                            </div>
                          </li>
                        ))}
                      </ul>
                    );
                  case "keyTakeaways":
                    return keyTakeaways.map((data, index) => (
                      <li key={index} className="mb-2 list-disc pl-5">
                        <span className="text-md text-gray-800">
                          {data.point}
                        </span>
                      </li>
                    ));
                  default:
                    return null;
                }
              })()}
          </div>
        </motion.div>
      ))}
      {loading && (
        <div className="w-full mt-10 flex justify-center">
          <RotatingLines
            visible={true}
            width="50"
            strokeColor="#6F42C1"
            strokeWidth="5"
            animationDuration="0.75"
            ariaLabel="rotating-lines-loading"
          />
        </div>
      )}
    </div>
  );
};

export default MainForm;
