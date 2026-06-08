import { useDispatch, useSelector } from "react-redux";
import { useEffect } from "react";
import { CardComponent } from "../../../../common/CardComponent";
import { fetchMetrics } from "../../../../../hook/fetchMetrics";
import { setSection3DataReducer } from "../../../../../Store/Slices/Section3/section3Slice";

function Section3() {
  const dispatch = useDispatch();
  

  useEffect(() => {
    const url = "http://127.0.0.1:8000/api/dashboard/section3"
    const sectiondata = fetchMetrics(url)
    .then((sectiondata)=>{
      console.log(sectiondata);
      dispatch(setSection3DataReducer(sectiondata));
    })
  }, []); // Empty array ensures this only runs ONCE when the component mounts



  return (
    <div>Section3</div>
  )
}

export default Section3