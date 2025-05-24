import dotenv from 'dotenv';
dotenv.config();
import { ocr } from "llama-ocr";

async function runOCR(imagePath) {
  try {
    const markdown = await ocr({
      filePath: imagePath,
      apiKey: process.env.TOGETHER_API_KEY,
    });
    console.log(markdown);  // Print OCR result to be captured in Python
  } catch (error) {
    console.error("Error during OCR:", error);
    process.exit(1);
  }
}

// Get image path from command-line argument
const imagePath = process.argv[2];

if (!imagePath) {
  console.error("Please provide an image path as an argument.");
  process.exit(1);
}

runOCR(imagePath);
