-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 10, 2024 at 01:06 PM
-- Server version: 8.0.39
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `library_management`
--

-- --------------------------------------------------------

--
-- Table structure for table `books`
--

CREATE TABLE `books` (
  `id` int NOT NULL,
  `category_id` int NOT NULL,
  `title` varchar(100) NOT NULL,
  `publish_year` year NOT NULL,
  `author` varchar(100) NOT NULL,
  `publisher` varchar(100) NOT NULL,
  `summary` text,
  `cover` varchar(255) DEFAULT NULL,
  `view_count` int DEFAULT '0',
  `download_count` int DEFAULT '0',
  `file_path` varchar(255) DEFAULT NULL,
  `average_rating` float DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `books`
--

INSERT INTO `books` (`id`, `category_id`, `title`, `publish_year`, `author`, `publisher`, `summary`, `cover`, `view_count`, `download_count`, `file_path`, `average_rating`) VALUES
(1, 3, 'The Arabian Nights\r\n', '2008', 'Andrew Lang\r\n\r\n', 'Project Gutenberg\r\n\r\n', 'A medieval Middle-Eastern literary epic which tells the story of Scheherazade, a Sassanid Queen, who must relate a series of stories to her malevolent husband, the King, to delay her execution. The stories are told over a period of one thousand and one nights, and every night she ends the story with a suspenseful situation, forcing the King to keep her alive for another day. The individual stories were created over many centuries, by many people and in many styles, and they have become famous in their own right.\r\n\r\n', 'books/covers/The-Arabian-Nights.jpg', 0, 0, 'books/pdfs/The Arabian Nights.pdf', 0),
(2, 3, 'Lady Tanglewood\r\n', '2021', 'Toni Cabell\r\n\r\n', 'Endwood Press LLC\r\n\r\n', 'Nari knows the rumors about Arrowood. Forbidden magic. Illegal crossbreeding. Strange howls in the night. Should she go through with the wedding anyway? As Nari rides toward Arrowood and her new home, her head is elsewhere. Soon, she will be marrying the clan chief’s handsome son. Their rites of binding must go off without a hitch. Every detail of the ceremony needs to demonstrate unity between the two rival clans, as Nari of Tanglewood weds Mordahn of Arrowood. Nari hears the sound of horses’ hooves pounding the trail up ahead and frowns. Why is her fiancé riding out to greet her, here in this isolated stretch of road, wearing chainmail and bearing arms?\r\n\r\n', 'books/covers/Lady-Tanglewood.jpg', 0, 0, 'books/pdfs/Lady-Tanglewood.pdf', 0),
(3, 5, 'Dirt Dealers\r\n', '2023', 'A.W. Kaylen\r\n\r\n', 'A.W. Kaylen\r\n\r\n', 'A sex scandal. A string of murders. A top secret no one is allowed to know. A seemingly ordinary murder case is assigned to young FBI Special Agent Heather Chase. Little does she know she is about to walk into a dangerous web of deceptions and lies… Why is the FBI involved? The NYPD has plenty of talent. Why is her boss there? He never graced his presence at such lowly murder cases before… Something is off from the get go… Chase feels it in her gut, but can’t put her finger on. When highly trained assassins make repeated attempts on her life, she realizes that she must be onto something big. Realizing the hunter has become the hunted, Chase doubles down; but she has no one she can trust. She instinctively remembers and utilizes her special gift she didn’t know she had… The puzzle pieces finally fall into place and the murder case wraps up… Except… Chase can’t help shaking the feeling that everything is nothing but a complete setup. Will she be able to prove it?\r\n\r\n', 'books/covers/Dirt-Dealers.jpg', 0, 0, 'books/pdfs/dirt-dealers.pdf', 0),
(4, 3, 'War Of The Animals\r\n', '2023', 'Jonathan DeCoteau\r\n\r\n', 'Animus Nor Books\r\n\r\n', 'War breaks out. This time, nature fights back... A failed effort to weaponize animals awakens their intellects. The military responds by creating death camps to exterminate infected animals. Moon Shadow, an Arctic white wolf, unites with White Claw, a polar bear king, to form Animus Nor, the first animal republic, to negotiate peace. The uneasy peace is broken with the rise of Azaz, lord of the grizzly bears. Azaz attacks human settlements, considering humans an invasive species that wreaks havoc on bears and the environment. A world war breaks out as animals face humans and each other to see who will become the true apex species. Will humanity win, or will nature triumph in the end?\r\n\r\n', 'books/covers/War-Of-The-Animals.jpg', 0, 0, 'books/pdfs/War Of The Animals.pdf', 0),
(5, 8, 'Billionaire Boss Protector\r\n', '2023', 'Tessa Sloan\r\n\r\n', 'Wild Fern Publishing, LLC\r\n\r\n', 'I’m secretly in love with the man who’s been protecting me for the past 3 years, But he sees me as nothing more than a liability. Derik Lewis is insufferable. Cold. Despotic. If he were only my boss, life would be agonizing enough. But he’s more than that. He’s my guardian and mentor. My grandfather appointed him to watch over me until I’m ready to take over the family business. I shouldn’t want him, but I can’t stop myself. Neither can he. But coming together only tears us farther apart. Now he’s gone. When danger looms and tragedy strikes, a long-kept family secret is discovered that has the potential to change everything. If only he’ll return to me.\r\n\r\n', 'books/covers/Billionaire-Boss-Protector.jpg', 0, 0, 'books/pdfs/Billionaire-Boss-Protector.pdf', 0),
(6, 7, 'Hunted by the Past\r\n', '2018', 'Jami Gray\r\n\r\n', 'Celtic Moon Press\r\n\r\n', 'She’s a reluctant psychic. He’s the man who walked away. Can they see beyond their painful past to survive a sadistic killer’s lethal game of revenge? No matter how far she runs, she can’t escape… Changing the past is an impossibility ex-Marine, Cynthia “Cyn” Arden, understands all too well. Struggling in the aftermath of a botched mission, which cost her two teammates, her military career, and a fledging relationship, her world’s upended once more by a panicked phone call. The psychic killer behind her nightmares has escaped military custody and is hunting down her remaining teammates, one by one. Up next on his murderous list—Cyn. Unless she can trust the one who walked away… The killer’s game brings her face to face with the one person guaranteed to throw her off kilter—the unsettling and distracting man she left behind, Kayden Shaw. Once she believed he’d stand by her side, then he chose his job and secrets over her, leaving her heart scarred by their tumultuous past.\r\n\r\n', 'books/covers/Hunted-by-the-Past.png', 0, 0, 'books/pdfs/Hunted-by-the-Past.pdf', 0),
(7, 1, 'The Diary of a Young Girl', '1947', 'Anne Frank', 'Contact Publishing', 'The diary of a young girl hiding during WWII.', 'books/covers/Anne_Frank.jpg', 0, 0, 'books/pdfs/Anne-Frank-The-Diary-Of-A-Young-Girl.pdf', 4.8),
(8, 1, 'Long Walk to Freedom', '1994', 'Nelson Mandela', 'Macdonald Purnell', 'Autobiography of Nelson Mandela.', 'books/covers/Nelson_Mandela.jpg', 0, 0, 'books/pdfs/the-autobiography-of-nelson-mandela.pdf', 4.7),
(9, 2, 'Good Omens', '1990', 'Neil Gaiman & Terry Pratchett', 'Gollancz', 'A comedic novel about the apocalypse.', 'books/covers/Neil_Gaiman&Terry_Pratchett.jpg', 0, 0, 'books/pdfs/Good.pdf', 4.6),
(10, 2, 'Bossypants', '2011', 'Tina Fey', 'Little, Brown and Company', 'Memoir by comedian Tina Fey.', 'books/covers/Tina_Fey.jpg', 0, 0, 'books/pdfs/Bossypants.pdf', 4.5),
(11, 3, 'Harry Potter and the Sorcerers Stone', '1997', 'J.K. Rowling', 'Bloomsbury', 'The first book in the Harry Potter series.', 'books/covers/J.K.Rowling.jpg', 0, 0, 'books/pdfs/harrypotter.pdf', 4.9),
(12, 3, 'The Hobbit', '1937', 'J.R.R. Tolkien', 'George Allen & Unwin', 'The prelude to the Lord of the Rings.', 'books/covers/J.R.R.Tolkien.jpg', 0, 0, 'books/pdfs/the-hobbit-1.pdf', 4.8),
(13, 4, 'Dune', '1965', 'Frank Herbert', 'Chilton Books', 'A classic science fiction novel set on the desert planet Arrakis.', 'books/covers/Frank_Herbert.jpg', 0, 0, 'books/pdfs/Dune by Frank Herbert.pdf', 4.6),
(14, 4, 'Neuromancer', '1984', 'William Gibson', 'Ace', 'A novel that popularized the concept of cyberspace.', 'books/covers/William_Gibson.jpg', 0, 0, 'books/pdfs/neuromancer.pdf', 4.5),
(15, 5, 'The Girl with the Dragon Tattoo', '2005', 'Stieg Larsson', 'Norstedts Förlag', 'A mystery thriller about a journalist and a hacker.', 'books/covers/Stieg_Larsson.jpg', 0, 0, 'books/pdfs/the_girl_with_the_dragon_tattoo.pdf', 4.4),
(16, 5, 'Gone Girl', '2012', 'Gillian Flynn', 'Crown Publishing', 'A psychological thriller about a missing wife.', 'books/covers/Gillian_Flynn.jpg', 0, 0, 'books/pdfs/Gone-Girl-Gillian-Flynn.pdf', 4.6),
(17, 11, 'The Innovators', '2014', 'Walter Isaacson', 'Simon & Schuster', 'A history of the pioneers of the digital revolution.', 'books/covers/Walter_Isaacson.jpg', 0, 0, 'books/pdfs/the-innovators.pdf', 4.6),
(18, 6, 'A Brief History of Time', '1988', 'Stephen Hawking', 'Bantam Books', 'An exploration of cosmology by Stephen Hawking.', 'books/covers/Stephen_Hawking.jpg', 0, 0, 'books/pdfs/A Brief History of Time - Stephen Hawking.pdf', 4.7),
(19, 6, 'Thinking, Fast and Slow', '2011', 'Daniel Kahneman', 'Farrar, Straus and Giroux', 'Insights into human thinking and biases.', 'books/covers/Daniel_Kahneman.jpg', 0, 0, 'books/pdfs/Daniel-Kahneman-Thinking-Fast-and-Slow-.pdf', 4.6),
(20, 7, 'It', '1986', 'Stephen King', 'Viking', 'A horror novel about a malevolent entity in Derry.', 'books/covers/Stephen_King.jpg', 0, 0, 'books/pdfs/it-by-stephen-king.pdf', 4.5),
(21, 7, 'The Haunting of Hill House', '1959', 'Shirley Jackson', 'Viking', 'A psychological horror novel about a haunted house.', 'books/covers/Shirley_Jackson.jpg', 0, 0, 'books/pdfs/jackson-shirley-the-haunting-of-hill-house.pdf', 4.3),
(22, 8, 'The Notebook', '1996', 'Nicholas Sparks', 'Warner Books', 'A romance novel about enduring love.', 'books/covers/Nicholas_Sparks.jpg', 0, 0, 'books/pdfs/excerpt-1.1996.10-the-notebook.pdf', 4.4),
(23, 9, 'Watchmen', '1986', 'Alan Moore', 'DC Comics', 'A graphic novel depicting a dystopian alternate history.', 'books/covers/Alan_Moore.jpg', 0, 0, 'books/pdfs/watchmen-ch.-1.pdf', 4.7),
(24, 9, 'The Sandman', '1989', 'Neil Gaiman', 'DC Comics', 'A comic series that follows Dream of the Endless.', 'books/covers/Neil_Gaiman.jpg', 0, 0, 'books/pdfs/sandman.pdf', 4.6),
(25, 10, 'To Kill a Mockingbird', '1960', 'Harper Lee', 'J.B. Lippincott & Co.', 'A novel about racial injustice in the Deep South.', 'books/covers/Harper_Lee.jpg', 0, 0, 'books/pdfs/TKMFullText.pdf', 4.9),
(26, 10, 'The Great Gatsby', '1925', 'F. Scott Fitzgerald', 'Scribner', 'A novel about the American dream and society in the 1920s.', 'books/covers/F.Scott_Fitzgerald.jpg', 0, 0, 'books/pdfs/the-great-gatsby.pdf', 4.8),
(27, 11, 'Sapiens: A Brief History of Humankind', '2011', 'Yuval Noah Harari', 'Harvill Secker', 'A narrative history of humankind.', 'books/covers/Yuval_Noah_Harari.jpg', 0, 0, 'books/pdfs/Sapiens-A-Brief-History-of-Humankind.pdf', 4.7);

-- --------------------------------------------------------

--
-- Table structure for table `category`
--

CREATE TABLE `category` (
  `id` int NOT NULL,
  `category` varchar(50) NOT NULL,
  `image` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `category`
--

INSERT INTO `category` (`id`, `category`, `image`) VALUES
(1, 'Biography', 'category/Biography.png'),
(2, 'Comedy', 'category/Comedy.png'),
(3, 'Fantasy', 'category/Fantasy.jpg'),
(4, 'Science-Fiction', 'category/Science-Fiction.jpg'),
(5, 'Mystery', 'category/Mystery.jpg'),
(6, 'Education', 'category/Education.jpg'),
(7, 'Horror', 'category/Horror.jpg'),
(8, 'Romance', 'category/Romance.jpg'),
(9, 'Comic', 'category/Comic.jpg'),
(10, 'Novel', 'category/novel.jpg'),
(11, 'Science & Technology', 'category/Science-and-Technology.jpg');

-- --------------------------------------------------------

--
-- Table structure for table `comments`
--

CREATE TABLE `comments` (
  `id` int NOT NULL,
  `book_id` int NOT NULL,
  `student_id` varchar(10) NOT NULL,
  `content` text NOT NULL,
  `created_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `favorites`
--

CREATE TABLE `favorites` (
  `id` int NOT NULL,
  `book_id` int NOT NULL,
  `student_id` varchar(10) NOT NULL,
  `added_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `ratings`
--

CREATE TABLE `ratings` (
  `id` int NOT NULL,
  `book_id` int NOT NULL,
  `student_id` varchar(10) NOT NULL,
  `rating` tinyint NOT NULL,
  `created_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `update_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `students`
--

CREATE TABLE `students` (
  `id` varchar(10) NOT NULL,
  `fullname` varchar(100) NOT NULL,
  `gender` varchar(5) NOT NULL,
  `class_name` varchar(50) NOT NULL,
  `username` varchar(100) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(100) NOT NULL,
  `avatar` varchar(255) DEFAULT NULL,
  `role` enum('user','admin') NOT NULL DEFAULT 'user',
  `created_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `is_active` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `students`
--

INSERT INTO `students` (`id`, `fullname`, `gender`, `class_name`, `username`, `email`, `password`, `avatar`, `role`, `created_on`, `updated_on`, `is_active`) VALUES
('102220335', 'Tran Quoc', 'Male', '22T_Nhat2', 'tranquoc1301', 'tranquoc1301@gmail.com', '$2b$12$iJgOlvlJfzfUGo1XVVxP2O1TbSWBOAZGyZ7HLf9OPZnZ45oMjW0Cy', 'avatars/Night_City.png', 'user', '2024-11-09 02:57:35', '2024-11-10 08:46:38', 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `books`
--
ALTER TABLE `books`
  ADD PRIMARY KEY (`id`),
  ADD KEY `category_id` (`category_id`);

--
-- Indexes for table `category`
--
ALTER TABLE `category`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `unique_category` (`category`);

--
-- Indexes for table `comments`
--
ALTER TABLE `comments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `book_id` (`book_id`),
  ADD KEY `student_id` (`student_id`);

--
-- Indexes for table `favorites`
--
ALTER TABLE `favorites`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `book_id` (`book_id`,`student_id`),
  ADD KEY `student_id` (`student_id`);

--
-- Indexes for table `ratings`
--
ALTER TABLE `ratings`
  ADD PRIMARY KEY (`id`),
  ADD KEY `book_id` (`book_id`),
  ADD KEY `student_id` (`student_id`);

--
-- Indexes for table `students`
--
ALTER TABLE `students`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `books`
--
ALTER TABLE `books`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=29;

--
-- AUTO_INCREMENT for table `category`
--
ALTER TABLE `category`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `comments`
--
ALTER TABLE `comments`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `favorites`
--
ALTER TABLE `favorites`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `ratings`
--
ALTER TABLE `ratings`
  MODIFY `id` int NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `books`
--
ALTER TABLE `books`
  ADD CONSTRAINT `books_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `category` (`id`);

--
-- Constraints for table `comments`
--
ALTER TABLE `comments`
  ADD CONSTRAINT `comments_fk_book` FOREIGN KEY (`book_id`) REFERENCES `books` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `comments_fk_student` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `favorites`
--
ALTER TABLE `favorites`
  ADD CONSTRAINT `favorites_fk_book` FOREIGN KEY (`book_id`) REFERENCES `books` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `favorites_fk_student` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `ratings`
--
ALTER TABLE `ratings`
  ADD CONSTRAINT `ratings_fk_book` FOREIGN KEY (`book_id`) REFERENCES `books` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `ratings_fk_student` FOREIGN KEY (`student_id`) REFERENCES `students` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
