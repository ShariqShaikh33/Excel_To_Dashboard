import { configureStore } from "@reduxjs/toolkit";
import section1Slice from "./Slices/Section1/section1Slice";
import section2Slice from "./Slices/Section2/section2Slice";
import section3Slice from "./Slices/Section3/section3Slice";

export const store = configureStore({
    reducer:{
        section1: section1Slice,
        section2: section2Slice,
        section3: section3Slice
    }
});