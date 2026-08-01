# Month 02 Resources

Tài liệu dưới đây dùng cho Month-02. Chỉ đọc phần được chỉ định trong từng ngày; không cần đọc toàn bộ website.

## Tuần 1 - Data processing

- NumPy: [NumPy absolute beginners](https://numpy.org/doc/stable/user/absolute_beginners.html) - đọc phần import convention, array fundamentals, shape, dtype, aggregation.
- NumPy: [NumPy quickstart](https://numpy.org/doc/stable/user/quickstart.html) - đọc phần basics, array creation, indexing và basic operations.
- pandas: [10 minutes to pandas](https://pandas.pydata.org/docs/user_guide/10min.html) - đọc phần DataFrame, viewing data, selection, missing data.
- pandas: [Working with missing data](https://pandas.pydata.org/docs/user_guide/missing_data.html) - đọc phần detecting, filling và dropping missing values.
- scikit-learn: [train_test_split](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html) - đọc tham số `test_size`, `random_state`, `shuffle`, `stratify`.

## Tuần 2 - ML baseline và metrics

- scikit-learn: [Linear Models](https://scikit-learn.org/stable/modules/linear_model.html) - đọc Linear Regression overview và Logistic Regression section.
- scikit-learn API: [LogisticRegression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html) - đọc mục purpose, input expectation, regularization default.
- scikit-learn: [Model evaluation: classification metrics](https://scikit-learn.org/stable/modules/model_evaluation.html#classification-metrics) - đọc accuracy, precision, recall, F1, confusion matrix.
- scikit-learn: [OneHotEncoder](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.OneHotEncoder.html) - đọc purpose, `handle_unknown` và output.
- scikit-learn: [StandardScaler](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.StandardScaler.html) - đọc khi nào cần scaling và vì sao fit trên train.

## Tuần 3 - PyTorch training loop

- PyTorch: [Learn the Basics](https://docs.pytorch.org/tutorials/beginner/basics/intro.html) - đọc overview các phần Tensors, Dataset/DataLoader, Build Model, Autograd, Optimization.
- PyTorch: [Datasets and DataLoaders](https://docs.pytorch.org/tutorials/beginner/basics/data_tutorial.html) - đọc cách viết Dataset và dùng DataLoader.
- PyTorch: [Build the Neural Network](https://docs.pytorch.org/tutorials/beginner/basics/buildmodel_tutorial.html) - đọc `nn.Module`, layers và forward pass.
- PyTorch: [Automatic Differentiation](https://docs.pytorch.org/tutorials/beginner/basics/autogradqs_tutorial.html) - đọc gradient tracking ở mức khái niệm.
- PyTorch: [Optimizing Model Parameters](https://docs.pytorch.org/tutorials/beginner/basics/optimization_tutorial.html) - đọc training loop, validation loop, loss và optimizer.

## Tuần 4 - Transformer foundation

- Hugging Face Course: [How do Transformers work?](https://huggingface.co/docs/course/main/en/chapter1/4) - đọc attention layers và encoder/decoder overview.
- Hugging Face Course: [Transformer Architectures](https://huggingface.co/docs/course/chapter1/6) - đọc encoder-only, decoder-only và encoder-decoder.
- Hugging Face Transformers: [Glossary](https://huggingface.co/docs/transformers/main/glossary) - đọc attention mask, autoregressive models, causal language modeling, embeddings nếu cần tra cứu.
- Jay Alammar: [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/) - dùng như nguồn trực quan cho self-attention, Q/K/V, multi-head attention và positional encoding.
- PyTorch API: [torch.nn.Transformer](https://docs.pytorch.org/docs/stable/generated/torch.nn.modules.transformer.Transformer.html) - chỉ đọc purpose và shape notes, không cần dùng trong production.

## Ghi chú sử dụng nguồn

- Ưu tiên đọc tài liệu chính thức trước, bài giải thích trực quan sau.
- Nếu một trang docs đổi version, giữ nguyên ý chính và kiểm tra lại API trước khi áp dụng vào code.
- Không copy nguyên văn dài vào `docs/transformer-foundation.md`; hãy viết lại bằng lời của người học và trích link nguồn.
