import { useDispatch, useSelector } from "react-redux";
import { setSection1DataReducer } from "../../../../../Store/Slices/Section1/section1Slice";
import { useEffect } from "react";
import { CardComponent } from "../../../../common/CardComponent";
import { fetchMetrics } from "../../../../../hook/fetchMetrics";
import { section1Selector } from "../../../../../Store/Slices/Section1/section1Selector";

function Section1() {
  const dispatch = useDispatch();
  const section1Data = useSelector(section1Selector)
  console.log(section1Data);
  
  useEffect(() => {
    const url = "http://127.0.0.1:8000/api/dashboard/section1";
    const sectiondata = fetchMetrics(url)
    .then((sectiondata)=>{
      console.log(sectiondata.gender_distribution);
      dispatch(setSection1DataReducer(sectiondata));
    });
  }, []); // Empty array ensures this only runs ONCE when the component mounts


  return (
    <div className='flex '>
      {
        section1Data?.gender_distribution?.map((i)=>{
          return <CardComponent key={i.gender} title={i.gender} value={i.count} subtext={i.percentage}/>
        })
      }
    </div>
  )
}

export default Section1